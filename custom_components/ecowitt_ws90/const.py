"""Constants for the Ecowitt WS90 integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ecowitt_ws90"

CONF_UNIT_ID = "unit_id"

DEFAULT_PORT = 502
# The WS90's factory-default Modbus device address.
DEFAULT_UNIT_ID = 0x90
