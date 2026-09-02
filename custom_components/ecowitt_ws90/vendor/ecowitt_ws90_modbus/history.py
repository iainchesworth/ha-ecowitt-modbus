"""Rolling 30-minute per-minute history archived by the WS90.

Registers 0x9B14-0x9C5D (added in Modbus RTU spec v1.0.6). Each of the 11
parameters below is its own contiguous run of 30 registers, one sample per
minute: index 0 is the most recent minute, index 29 is 30 minutes ago.
Battery and capacitance voltage are not available anywhere in the live
register block (see :mod:`.sensors`) -- this history is the only way to read
them.
"""

from __future__ import annotations

from modbus_connection.model import Component, gauge, integer, repeating_group

_INVALID = 0xFFFF
_SAMPLES = 30


class _MaxLightSample(Component):
    """One archived minute of maximum light intensity."""

    value = gauge(0x9B14, 10, signed=False, nan=_INVALID, unit="lx")


class _MaxUvIndexSample(Component):
    """One archived minute of maximum UV index."""

    value = gauge(0x9B32, 0.1, signed=False, nan=_INVALID)


class _AvgTemperatureSample(Component):
    """One archived minute of average temperature."""

    value = gauge(0x9B50, 0.1, offset=-40, signed=False, nan=_INVALID, unit="°C")


class _AvgHumiditySample(Component):
    """One archived minute of average humidity."""

    value = integer(0x9B6E, signed=False, nan=_INVALID, unit="%")


class _AvgWindSpeedSample(Component):
    """One archived minute of average wind speed."""

    value = gauge(0x9B8C, 0.1, signed=False, nan=_INVALID, unit="m/s")


class _MaxGustSpeedSample(Component):
    """One archived minute of maximum gust speed."""

    value = gauge(0x9BAA, 0.1, signed=False, nan=_INVALID, unit="m/s")


class _AvgWindDirectionSample(Component):
    """One archived minute of average wind direction."""

    value = integer(0x9BC8, signed=False, nan=_INVALID, unit="°")


class _RainfallSample(Component):
    """One archived minute of rainfall.

    The spec does not document a sentinel for this register, unlike the other
    ten history arrays; 0xFFFF (655.35mm in one minute) can never be a
    genuine reading, so it is applied defensively anyway.
    """

    value = gauge(0x9BE6, 0.1, signed=False, nan=_INVALID, unit="mm")


class _AvgAbsolutePressureSample(Component):
    """One archived minute of average absolute pressure."""

    value = gauge(0x9C04, 0.1, signed=False, nan=_INVALID, unit="hPa")


class _AvgBatteryVoltageSample(Component):
    """One archived minute of average battery voltage."""

    value = gauge(0x9C22, 0.01, signed=False, nan=_INVALID, unit="V")


class _AvgCapacitanceVoltageSample(Component):
    """One archived minute of average capacitance (solar storage) voltage."""

    value = gauge(0x9C40, 0.1, signed=False, nan=_INVALID, unit="V")


class History(Component):
    """The last 30 one-minute samples of each archived reading."""

    max_light = repeating_group(_SAMPLES, _MaxLightSample, stride=1)
    max_uv_index = repeating_group(_SAMPLES, _MaxUvIndexSample, stride=1)
    avg_temperature = repeating_group(_SAMPLES, _AvgTemperatureSample, stride=1)
    avg_humidity = repeating_group(_SAMPLES, _AvgHumiditySample, stride=1)
    avg_wind_speed = repeating_group(_SAMPLES, _AvgWindSpeedSample, stride=1)
    max_gust_speed = repeating_group(_SAMPLES, _MaxGustSpeedSample, stride=1)
    avg_wind_direction = repeating_group(_SAMPLES, _AvgWindDirectionSample, stride=1)
    rainfall = repeating_group(_SAMPLES, _RainfallSample, stride=1)
    avg_absolute_pressure = repeating_group(
        _SAMPLES, _AvgAbsolutePressureSample, stride=1
    )
    avg_battery_voltage = repeating_group(_SAMPLES, _AvgBatteryVoltageSample, stride=1)
    avg_capacitance_voltage = repeating_group(
        _SAMPLES, _AvgCapacitanceVoltageSample, stride=1
    )

    @property
    def battery_voltage(self) -> float | None:
        """The most recently archived minute's average battery voltage."""
        samples = self.avg_battery_voltage
        return samples[0].value if samples else None

    @property
    def capacitance_voltage(self) -> float | None:
        """The most recently archived minute's average capacitance voltage."""
        samples = self.avg_capacitance_voltage
        return samples[0].value if samples else None
