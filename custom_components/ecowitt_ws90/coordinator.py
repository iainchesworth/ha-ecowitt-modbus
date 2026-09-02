"""Polling, and what to do when the sensor stops answering."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, override

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from modbus_connection import ModbusError
from propcache.api import cached_property

from .const import DOMAIN, LOGGER
from .vendor.ecowitt_ws90_modbus import WS90

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

SCAN_INTERVAL = timedelta(seconds=30)

type WS90ConfigEntry = ConfigEntry[WS90DataUpdateCoordinator]


class WS90DataUpdateCoordinator(DataUpdateCoordinator[WS90]):
    """Poll the WS90's live weather readings."""

    config_entry: WS90ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: WS90ConfigEntry,
        device: WS90,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=entry.title,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device

    @cached_property
    def device_info(self) -> DeviceInfo:
        """Return the device every entity on this config entry belongs to."""
        info = self.device.info
        return DeviceInfo(
            identifiers={(DOMAIN, f"{info.device_id:08x}")},
            manufacturer=info.manufacturer,
            model=info.model,
        )

    @override
    async def _async_update_data(self) -> WS90:
        try:
            await self.device.async_update()
        except ModbusError as err:
            message = f"Error communicating with the WS90: {err}"
            raise UpdateFailed(message) from err
        return self.device
