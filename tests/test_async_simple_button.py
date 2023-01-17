# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
"""
Tests for Simple Button implementation
"""
import sys
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, PropertyMock, AsyncMock

import digitalio

sys.modules["countio"] = MagicMock()

# pylint: disable=wrong-import-position
import async_button


class TestSimpleButton(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.countio = MagicMock()
        self.patch_countio = patch("async_button.countio", self.countio)
        self.patch_countio.start()
        self.counter = MagicMock()
        self.counter.__enter__.return_value = (
            self.counter
        )  # return self as a context manager
        type(self.counter).count = PropertyMock(side_effect=[0, 0, 1, 0, 0, 1])
        self.countio.Counter.return_value = self.counter
        self.asyncio = MagicMock()
        self.asyncio.sleep = AsyncMock()
        self.patch_asyncio = patch("async_button.asyncio", self.asyncio)
        self.patch_asyncio.start()
        self.edge_rise = self.countio.Edge.RISE
        self.edge_fall = self.countio.Edge.FALL

    def tearDown(self) -> None:
        self.patch_asyncio.stop()
        self.patch_countio.stop()

    async def test_pressed_active_high(self):
        button = async_button.SimpleButton("P1", True)
        await button.pressed()
        self.countio.Counter.assert_called_once_with(
            "P1", edge=self.edge_rise, pull=digitalio.Pull.DOWN
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_released_active_high(self):
        button = async_button.SimpleButton("P1", True)
        await button.released()
        self.countio.Counter.assert_called_once_with(
            "P1", edge=self.edge_fall, pull=digitalio.Pull.DOWN
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_pressed_active_low(self):
        button = async_button.SimpleButton("P1", False)
        await button.pressed()
        self.countio.Counter.assert_called_once_with(
            "P1", edge=self.edge_fall, pull=digitalio.Pull.UP
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_released_active_low(self):
        button = async_button.SimpleButton("P1", False)
        await button.released()
        self.countio.Counter.assert_called_once_with(
            "P1", edge=self.edge_rise, pull=digitalio.Pull.UP
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_pull_false_is_respected(self):
        button = async_button.SimpleButton("P1", False, pull=False)
        await button.released()
        self.countio.Counter.assert_called_once_with(
            "P1", edge=self.edge_rise, pull=None
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_default_interval(self):
        button = async_button.SimpleButton("P1", False)
        await button.pressed()
        self.asyncio.sleep.assert_awaited_with(0.05)
        await button.released()
        self.asyncio.sleep.assert_awaited_with(0.05)

    async def test_interval_zero(self):
        button = async_button.SimpleButton("P1", False, interval=0)
        await button.pressed()
        self.asyncio.sleep.assert_awaited_with(0)
        await button.released()
        self.asyncio.sleep.assert_awaited_with(0)

    async def test_other_interval(self):
        button = async_button.SimpleButton("P1", False, interval=1.25)
        await button.pressed()
        self.asyncio.sleep.assert_awaited_with(1.25)
        await button.released()
        self.asyncio.sleep.assert_awaited_with(1.25)
