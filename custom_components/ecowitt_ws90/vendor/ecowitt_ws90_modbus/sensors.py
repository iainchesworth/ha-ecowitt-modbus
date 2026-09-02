"""Live weather readings from the WS90 sensor array.

Registers 0x165-0x16E, refreshed by the manufacturer every 8.75s (light, UV,
temperature, humidity, rainfall, absolute pressure) or every 2s (wind speed,
gust speed, wind direction) -- polling faster than that does not return newer
data.
"""

from __future__ import annotations

from modbus_connection.model import Component, gauge, integer

# The spec explicitly documents 0xFFFF as "invalid" for every field below
# except rainfall and the rain counter; it is kept as the sentinel for those
# two as well since a raw 0xFFFF (655.35mm/6553.5mm) can never be a genuine
# reading and the legacy `modbus:` YAML config this library replaces already
# treated it as invalid across the board.
_INVALID = 0xFFFF


class Sensors(Component):
    """The WS90's live weather readings."""

    light = gauge(0x165, 10, signed=False, nan=_INVALID, unit="lx")
    uv_index = gauge(0x166, 0.1, signed=False, nan=_INVALID)
    temperature = gauge(0x167, 0.1, offset=-40, signed=False, nan=_INVALID, unit="°C")
    humidity = integer(0x168, signed=False, nan=_INVALID, unit="%")
    wind_speed = gauge(0x169, 0.1, signed=False, nan=_INVALID, unit="m/s")
    gust_speed = gauge(0x16A, 0.1, signed=False, nan=_INVALID, unit="m/s")
    wind_direction = integer(0x16B, signed=False, nan=_INVALID, unit="°")
    # 0.1mm resolution; the manufacturer's recommended rain total (see RainCounter
    # below for the finer-resolution alternative).
    rainfall = gauge(0x16C, 0.1, signed=False, nan=_INVALID, unit="mm")
    absolute_pressure = gauge(0x16D, 0.1, signed=False, nan=_INVALID, unit="hPa")
    # 0.01mm resolution; the same cumulative rain total as `rainfall`, just
    # read from a separate register with finer granularity.
    rain_counter = gauge(0x16E, 0.01, signed=False, nan=_INVALID, unit="mm")
