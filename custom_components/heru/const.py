"""Constants file"""

from homeassistant.const import Platform
from homeassistant.const import __version__ as HA_VERSION

NAME = "HERU"
DOMAIN = "heru"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"
ISSUE_URL = "https://github.com/toringer/home-assistant-heru/issues"

# Icons
ICON = "mdi:flash"
ICON_BATTERY_50 = "mdi:battery-50"
ICON_CASH = "mdi:cash"
ICON_CONNECTION = "mdi:connection"
ICON_MIN_SOC = "mdi:battery-charging-30"
ICON_START = "mdi:play-circle-outline"
ICON_STOP = "mdi:stop-circle-outline"
ICON_TIME = "mdi:clock-time-four-outline"

# Platforms
SENSOR = Platform.SENSOR
SWITCH = Platform.SWITCH
BUTTON = Platform.BUTTON
NUMBER = Platform.NUMBER
SELECT = Platform.SELECT
CLIMATE = Platform.CLIMATE
PLATFORMS = [SENSOR, SWITCH, BUTTON, CLIMATE]
# PLATFORMS = [SWITCH, SENSOR, BUTTON, NUMBER, SELECT]


# Configuration and options
CONF_HOST_NAME = "host_name"
CONF_HOST_PORT = "host_port"
CONF_DEVICE_NAME = "device_name"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
Home Assistant: {HA_VERSION}
-------------------------------------------------------------------
"""
