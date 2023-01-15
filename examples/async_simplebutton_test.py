# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: Unlicense
import asyncio

import board
import digitalio

import async_button

# green = digitalio.DigitalInOut(board.D9)
# red = digitalio.DigitalInOut(board.D8)
# blue = digitalio.DigitalInOut(board.D7)


async def counter():
    i = 0
    while True:
        print(f"COUNTER: {i}")
        await asyncio.sleep(1)
        i += 1


async def button_watcher():
    button = async_button.SimpleButton(board.D5, value_when_pressed=False)
    led = digitalio.DigitalInOut(board.D8)
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    while True:
        await button.pressed()
        print("Button pressed")
        led.value = 0
        await button.released()
        print("Button released")
        led.value = 1


async def main():
    await asyncio.gather(counter(), button_watcher())


asyncio.run(main())
