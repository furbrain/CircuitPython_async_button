# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
from functools import partial
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock
import sys
import asyncio

sys.modules["countio"] = MagicMock()

import async_button  # pylint: disable=wrong-import-position

SINGLE = async_button.Button.SINGLE
DOUBLE = async_button.Button.DOUBLE
LONG = async_button.Button.LONG


async def wait_and_return(delay: float, click_type):
    await asyncio.sleep(delay)
    if isinstance(click_type, int):
        click_type = [click_type]
    return click_type


class TestButton(IsolatedAsyncioTestCase):
    # pylint: disable=invalid-name, too-many-public-methods
    def setUp(self) -> None:
        self.button_a = MagicMock(async_button.Button)
        self.button_a.wait = AsyncMock()
        self.button_b = MagicMock(async_button.Button)
        self.button_b.wait = AsyncMock()
        self.button_c = MagicMock(async_button.Button)
        self.button_c.wait = AsyncMock()

    def testInitialise(self):
        async_button.MultiButton(a=self.button_a, b=self.button_b, c=self.button_c)

    def testInitialiseFailsWithNonButtons(self):
        with self.assertRaises(TypeError):
            async_button.MultiButton(a=self.button_a, b=self.button_b, c=12)

    async def testSimpleCase(self):
        multi = async_button.MultiButton(a=self.button_a)
        self.button_a.wait.return_value = [SINGLE]
        result = await multi.wait(a=SINGLE)
        self.assertEqual(("a", SINGLE), result)
        self.button_a.wait.assert_awaited_once()
        self.button_a.wait.assert_called_with(SINGLE)

    async def testTwoButtons(self):
        multi = async_button.MultiButton(a=self.button_a, b=self.button_b)
        self.button_a.wait = partial(wait_and_return, 0.2)
        self.button_b.wait = partial(wait_and_return, 0.1)
        result = await multi.wait(a=SINGLE, b=DOUBLE)
        self.assertEqual(("b", DOUBLE), result)

    async def testThreeButtons(self):
        multi = async_button.MultiButton(
            a=self.button_a, b=self.button_b, c=self.button_c
        )
        self.button_a.wait = partial(wait_and_return, 0.2)
        self.button_b.wait = partial(wait_and_return, 0.1)
        self.button_c.wait = partial(wait_and_return, 0.3)
        result = await multi.wait(a=SINGLE, b=DOUBLE, c=LONG)
        self.assertEqual(("b", DOUBLE), result)

    async def testOneButtonTwoClicks(self):
        multi = async_button.MultiButton(a=self.button_a)
        self.button_a.wait.return_value = [DOUBLE]
        result = await multi.wait(a=[SINGLE, DOUBLE])
        self.assertEqual(("a", DOUBLE), result)
        self.button_a.wait.assert_awaited_once()
        self.button_a.wait.assert_called_with([SINGLE, DOUBLE])
