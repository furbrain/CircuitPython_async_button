# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: Unlicense
import asyncio

import board
import digitalio

from microcontroller import Pin

from async_button import Button


def setUpLed(pin: Pin):
    dio = digitalio.DigitalInOut(pin)
    dio.direction = digitalio.Direction.OUTPUT
    dio.value = True
    return dio


CLICK_NAMES = {
    Button.SINGLE: "Single click",
    Button.DOUBLE: "Double click",
    Button.TRIPLE: "Triple click",
    Button.LONG: "Long click",
}


async def counter():
    i = 0
    while True:
        print(f"COUNTER: {i}")
        await asyncio.sleep(1)
        i += 1


async def button_led_watcher(button: Button, led: digitalio.DigitalInOut, click):
    while True:
        await button.wait((click,))
        led.value = False
        await asyncio.sleep(0.5)
        led.value = True


async def click_watcher(button: Button):
    while True:
        click = await button.wait_for_click()
        print(f"{CLICK_NAMES[click]} seen")


async def main():
    # note Button must be created in an async environment
    button = Button(
        board.D5,
        value_when_pressed=False,
        triple_click_enable=True,
        long_click_enable=True,
    )
    green = setUpLed(board.D9)
    red = setUpLed(board.D8)
    blue = setUpLed(board.D7)

    red_watcher = button_led_watcher(button, red, Button.SINGLE)
    green_watcher = button_led_watcher(button, green, Button.DOUBLE)
    blue_watcher = button_led_watcher(button, blue, Button.TRIPLE)
    await asyncio.gather(
        counter(), click_watcher(button), red_watcher, green_watcher, blue_watcher
    )


asyncio.run(main())
