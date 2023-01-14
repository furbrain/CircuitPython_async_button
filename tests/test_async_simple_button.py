# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
"""
Tests for Simple Button implementation
"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, PropertyMock, AsyncMock, Mock

import digitalio


class TestSimpleButton(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.countio = MagicMock()
        self.counter = MagicMock()
        self.counter.__enter__.return_value = (
            self.counter
        )  # return self as a context manager
        type(self.counter).count = PropertyMock(side_effect=[0, 0, 1])
        self.countio.Counter.return_value = self.counter
        self.asyncio = Mock()
        self.asyncio.sleep = AsyncMock()
        self.edge_rise = self.countio.Edge.RISE
        self.edge_fall = self.countio.Edge.FALL
        with patch.dict("sys.modules", countio=self.countio, asyncio=self.asyncio):
            # pylint: disable=import-outside-toplevel
            from async_button import SimpleButton

            self.simple_button_class = SimpleButton

    async def test_pressed_active_high(self):
        button = self.simple_button_class("P1", True)
        await button.pressed()
        self.countio.Counter.assert_called_once_with(
            "P1", self.edge_rise, digitalio.Pull.DOWN
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_released_active_high(self):
        button = self.simple_button_class("P1", True)
        await button.released()
        self.countio.Counter.assert_called_once_with(
            "P1", self.edge_fall, digitalio.Pull.DOWN
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_pressed_active_low(self):
        button = self.simple_button_class("P1", False)
        await button.pressed()
        self.countio.Counter.assert_called_once_with(
            "P1", self.edge_fall, digitalio.Pull.UP
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)

    async def test_released_active_low(self):
        button = self.simple_button_class("P1", False)
        await button.released()
        self.countio.Counter.assert_called_once_with(
            "P1", self.edge_rise, digitalio.Pull.UP
        )
        self.assertEqual(self.asyncio.sleep.await_count, 2)
