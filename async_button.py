# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
"""
`async_button`
================================================================================

a library for reading buttons using asyncio


* Author(s): Phil Underwood

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* CircuitPython asyncio module:
  https://github.com/adafruit/Adafruit_CircuitPython_asyncio
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/furbrain/CircuitPython_async_button.git"

import time

import asyncio
from typing import Dict, Sequence

import digitalio
import keypad
from microcontroller import Pin
import countio


class SimpleButton:
    """
    Asynchronous interface to a button or other IO input
    """

    def __init__(self, pin: Pin, value_when_pressed: bool, pull: bool = True):
        """

        :param Pin pin: Pin to wait for
        :param bool value_when_pressed: ``True`` if the pin reads high when the key is pressed.
          ``False`` if the pin reads low (is grounded) when the key is pressed.
        :param bool pull: ``True`` if an internal pull-up or pull-down should be enabled on the
          pin. A pull-up will be used if value_when_pressed is False; a pull-down will be used if
          it is ``True``. If an external pull is already provided for the pin, you can set
          pull to ``False``. However, enabling an internal pull when an external one is already
          present is not a problem; it simply uses slightly more current.
        """
        self.pin: Pin = pin
        self.value_when_pressed = value_when_pressed
        if pull:
            self.pull = digitalio.Pull.DOWN if value_when_pressed else digitalio.Pull.UP
        else:
            self.pull = None

    async def pressed(self):
        """
        Wait until pin is pressed
        :return:
        """
        edge = countio.Edge.RISE if self.value_when_pressed else countio.Edge.FALL
        with countio.Counter(self.pin, edge, self.pull) as counter:
            while True:
                if counter.count > 0:
                    return
                await asyncio.sleep(0)

    async def released(self):
        """
        Wait until pin is released
        :return:
        """
        edge = countio.Edge.FALL if self.value_when_pressed else countio.Edge.RISE
        with countio.Counter(self.pin, edge, self.pull) as counter:
            while True:
                if counter.count > 0:
                    return
                await asyncio.sleep(0)


class Button:
    # pylint: disable
    """
    This object will monitor the specified pin for changes and will report
    single, double, triple and long_clicks. It creates a background _`asyncio` process
    that will monitor the button.
    """

    PRESSED = 1
    RELEASED = 2
    SINGLE = 4
    DOUBLE = 8
    TRIPLE = 16
    LONG = 32
    ANY_CLICK = SINGLE | DOUBLE | TRIPLE | LONG

    def __init__(
        self,
        pin: Pin,
        value_when_pressed: bool,
        *,
        pull: bool = False,
        double_click_max_duration=0.5,
        long_click_min_duration=3.0,
        double_click_enable: bool = True,
        triple_click_enable: bool = False,
        long_click_enable: bool = False,
    ):
        """
        Create the button object and start the background async process, this object must be
        created only when the asyncio event loop is running
        :param Pin pin: the pin to be monitored
        :param bool value_when_pressed: ``True`` if the pin reads high when the key is pressed.
          ``False`` if the pin reads low (is grounded) when the key is pressed.
        :param bool pull: ``True`` if an internal pull-up or pull-down should be enabled on
        the pin. A pull-up will be used if ``value_when_pressed`` is ``False``; a pull-down will be
        used if it is True. If an external pull is already provided for the pins, you can set
        pull to ``False``. However, enabling an internal pull when an external one is already
        present is not a problem; it simply uses slightly more current.
        :param float double_click_max_duration: how long in seconds before a second click is
          registered as a double click (this is also the value used for triple clicks.
          Default is 0.5 seconds
        :param float long_click_min_duration: how long in seconds the button must be pressed before
          a long_click is triggered
        :param bool double_click_enable: Whether double clicks are detected. Default is True
        :param bool triple_click_enable: Whether triple clicks are detected. Default is False
        :param bool long_click_enable: Whether long clicks are detected. Default is False
        """
        self.pin = pin
        self.value_when_pressed = value_when_pressed
        self.double_click_max_duration = double_click_max_duration
        self.long_click_min_duration = long_click_min_duration
        self.click_enabled = {
            self.DOUBLE: double_click_enable,
            self.TRIPLE: triple_click_enable,
            self.LONG: long_click_enable,
        }
        self.keys = keypad.Keys(
            (self.pin,), value_when_pressed=value_when_pressed, pull=pull
        )
        self.monitor_task = asyncio.create_task(self._monitor())
        self.events = {
            x: asyncio.Event()
            for x in (
                self.SINGLE,
                self.DOUBLE,
                self.TRIPLE,
                self.LONG,
                self.PRESSED,
                self.RELEASED,
            )
        }
        self.last_click = None
        self.pressed = False

    async def _monitor(self):
        """
        This is the main background task that monitors key presses and releases
        :return:
        """
        evt = keypad.Event(0, False)
        last_click_tm = -100000
        long_click_due = None
        while True:
            if self.keys.events.get_into(evt):
                if evt.pressed:
                    self._trigger(self.pressed)
                    now = time.monotonic()
                    if now - last_click_tm < self.double_click_max_duration:
                        self._increase_clicks()
                    self.last_click_tm = now
                    long_click_due = now + self.long_click_min_duration
                    self.pressed = True
                else:
                    self._trigger(self.RELEASED)
                    self._trigger(self.last_click)
                    self.pressed = False
            else:
                if self.pressed and self.click_enabled[self.LONG]:
                    if (
                        time.monotonic() > long_click_due
                        and self.last_click != self.LONG
                    ):
                        self.last_click = self.LONG
                        self._trigger(self.LONG)
            await asyncio.sleep(0)

    def _increase_clicks(self):
        if self.last_click == self.SINGLE and self.click_enabled[self.DOUBLE]:
            self.last_click = self.DOUBLE
        elif self.last_click == self.DOUBLE and self.click_enabled[self.TRIPLE]:
            self.last_click = self.TRIPLE
        else:
            self.last_click = self.SINGLE

    def _trigger(self, event: int):
        evt = self.events[event]
        evt.set()
        evt.clear()

    async def wait(self, click_types: Sequence[int]):
        """
        Wait for the first of the specified events.
        :param List[int] click_types: One or more events to listen for.
        :return: A list of the clicks that actually happened.

        :example:

        >>>async def get_click():
        >>>    # wait for a double or triple click
        >>>    clicks = await button.wait((Button.DOUBLE, Button.TRIPLE))
        >>>    if Button.DOUBLE in clicks:
        >>>        # do something


        """
        evts: Dict[int, asyncio.Task] = {}
        for evt_type in click_types:
            evts[evt_type] = asyncio.create_task(self.events[evt_type].wait())
        await asyncio.wait(evts.values(), return_when=asyncio.FIRST_COMPLETED)
        if len(evts) > 1:
            await asyncio.sleep(0)  # ensure all event types get an opportunity to run
        results = []
        for evt_type, evt in evts.items():
            if evt.done():
                results.append(evt_type)
            else:
                evt.cancel()  # cancel unfired events
        return results

    def deinit(self):
        """
        Deinitialise this and stop the background task
        :return:
        """
        self.monitor_task.cancel()
        self.keys.deinit()
