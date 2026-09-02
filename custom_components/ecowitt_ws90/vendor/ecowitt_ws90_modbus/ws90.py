"""The WS90 as a single Modbus device object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modbus_connection.model import ComponentGroup

from .device_info import DeviceInfo
from .history import History
from .sensors import Sensors

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit


class WS90:
    """A Fine Offset / Ecowitt WS90 weather sensor array on Modbus."""

    def __init__(self, unit: ModbusUnit) -> None:
        self.info = DeviceInfo(unit)
        self.sensors = Sensors(unit)
        self.history = History(unit)
        # Identity (5 registers) and live readings (10 registers) sit right
        # next to each other on the device -- pool them into one read.
        self._live = ComponentGroup(unit, [self.info, self.sensors])

    async def async_update(self) -> None:
        """Refresh identity and live sensor readings in one pooled read.

        Raises ``ModbusExceptionError`` if the device rejects a block.
        """
        await self._live.async_update()

    async def async_update_history(self) -> None:
        """Refresh the last 30 minutes of archived readings.

        Polled separately from :meth:`async_update`: the history block is
        330 registers wide and changes only once a minute, so there is no
        reason to re-read it on every live poll.

        Raises ``ModbusExceptionError`` if the device rejects a block.
        """
        await self.history.async_update()
