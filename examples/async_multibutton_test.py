# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: Unlicense
import asyncio

import board

from async_button import Button, MultiButton

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


async def click_watcher(button: MultiButton):
    while True:
        button_name, click = await button.wait(a=Button.ANY_CLICK, b=Button.ANY_CLICK)
        print(f"{button_name}: {CLICK_NAMES[click]} seen")


async def main():
    # note Button must be created in an async environment
    button_a = Button(
        board.D3,
        value_when_pressed=False,
        long_click_enable=True,
    )
    button_b = Button(
        board.D4,
        value_when_pressed=False,
        long_click_enable=True,
    )
    multibutton = MultiButton(a=button_a, b=button_b)

    await asyncio.gather(counter(), click_watcher(multibutton))


asyncio.run(main())
