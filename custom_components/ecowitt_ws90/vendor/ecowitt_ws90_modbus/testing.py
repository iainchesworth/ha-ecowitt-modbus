"""Shared test fixtures for consumers of this library.

Exposes a captured register image so a consuming Home Assistant integration's
own tests can serve a plausible WS90 through ``modbus_connection``'s mock
backend without duplicating raw register values.
"""

from __future__ import annotations

# Raw holding-register words keyed by their (protocol) address. Reproduces
# Example 2 of Ecowitt's WS90ModbusRTU_V1.0.6 spec verbatim for the live
# block, plus that spec's own worked example for the rain counter register.
WS90_LIVE_EXAMPLE: dict[int, int] = {
    0x160: 0x90,  # device_code -> model "WS90"
    0x161: 2,  # baud_rate -> BAUD_9600
    0x162: 0x90,  # device_address (factory default)
    0x163: 0x1234,  # device_id MSB
    0x164: 0x5678,  # device_id LSB -> 0x12345678
    0x165: 1767,  # light -> 17670 lux
    0x166: 13,  # uv_index -> 1.3
    0x167: 662,  # temperature -> 26.2 C
    0x168: 60,  # humidity -> 60%
    0x169: 0,  # wind_speed -> 0.0 m/s
    0x16A: 0,  # gust_speed -> 0.0 m/s
    0x16B: 150,  # wind_direction -> 150 deg
    0x16C: 0,  # rainfall -> 0.0 mm
    0x16D: 10010,  # absolute_pressure -> 1001.0 hPa
    0x16E: 18,  # rain_counter -> 0.18 mm
}

# A WS90's factory-default device (slave) address, matching WS90_LIVE_EXAMPLE.
WS90_UNIT_ID = 0x90
