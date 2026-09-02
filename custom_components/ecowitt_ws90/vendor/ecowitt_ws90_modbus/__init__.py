"""ecowitt-ws90-modbus -- read a Fine Offset / Ecowitt WS90 weather sensor over Modbus.

Construct ``WS90(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as normal Python
objects::

    device.info.model
    device.sensors.temperature
    device.sensors.wind_speed

The last 30 minutes of archived per-minute readings (including battery and
capacitance voltage, not available anywhere else) are polled separately::

    await device.async_update_history()
    device.history.battery_voltage
"""

from .device_info import BaudRate, DeviceInfo
from .history import History
from .sensors import Sensors
from .ws90 import WS90

__all__ = [
    "WS90",
    "BaudRate",
    "DeviceInfo",
    "History",
    "Sensors",
]
