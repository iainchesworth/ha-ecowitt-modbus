"""Identity and RS-485 communication settings of the WS90."""

from __future__ import annotations

from enum import IntEnum

from modbus_connection.model import Component, enum, integer, uint32

# Register 0x160 only ever reports this one value on a genuine WS90; kept as a
# dict (rather than a bare constant) so an OEM variant sharing the map only
# needs a new entry here.
_MODEL_NAMES: dict[int, str] = {0x90: "WS90"}


class BaudRate(IntEnum):
    """Serial baud rates accepted by register 0x161."""

    BAUD_4800 = 1
    BAUD_9600 = 2
    BAUD_19200 = 3
    BAUD_115200 = 4


def _validate_device_address(value: int) -> int:
    """Reject a device (slave) address outside the WS90's accepted range.

    Raises ``ValueError`` if ``value`` is not 1-252.
    """
    if not 1 <= value <= 252:
        raise ValueError(f"device address must be between 1 and 252, got {value}")
    return value


class DeviceInfo(Component):
    """The WS90's identity and RS-485 communication settings."""

    device_code = integer(0x160, signed=False)
    baud_rate = enum(0x161, BaudRate, writable=True)
    device_address = integer(0x162, signed=False, writable=_validate_device_address)
    device_id = uint32(0x163)

    @property
    def manufacturer(self) -> str:
        """The sensor's manufacturer -- fixed, there is only ever one."""
        return "Ecowitt"

    @property
    def model(self) -> str | None:
        """The human-readable model name, or ``None`` before the first update."""
        if self.device_code is None:
            return None
        return _MODEL_NAMES.get(self.device_code, f"unknown (0x{self.device_code:02x})")
