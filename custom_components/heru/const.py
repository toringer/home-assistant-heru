"""Constants file"""

from homeassistant.const import Platform

NAME = "HERU"
DOMAIN = "heru"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

# Icon
ICON_FAN = "mdi:fan"
ICON_HEAT_WAVE = "mdi:heat-wave"
ICON_EXCHANGE = "mdi:swap-horizontal"
ICON_ALARM = "mdi:bell"
ICON_SWITCH = "mdi:electric-switch"

# Platforms
SENSOR = Platform.SENSOR
SWITCH = Platform.SWITCH
BUTTON = Platform.BUTTON
NUMBER = Platform.NUMBER
SELECT = Platform.SELECT
CLIMATE = Platform.CLIMATE
PLATFORMS = [SENSOR, SWITCH, BUTTON, CLIMATE]
# PLATFORMS = [SWITCH, SENSOR, BUTTON, NUMBER, SELECT]

# Modbus
DEFAULT_SLAVE = 1
REGISTER_HOLDING = "holding"
REGISTER_COILS = "coils"

# Configuration and options
CONF_HOST_NAME = "host_name"
CONF_HOST_PORT = "host_port"
CONF_DEVICE_NAME = "device_name"
CONF_DEVICE_MODEL = "device_model"


DEVICE_MODELS = [
    {"value": "heru_100s_ec", "label": "Heru 100S EC"},
    {"value": "heru_160s_ec", "label": "Heru 160S EC"},
    {"value": "heru_200s_ec", "label": "Heru 200S EC"},
    {"value": "heru_300s_ec", "label": "Heru 300S EC"},
    {"value": "heru_100t_ec", "label": "Heru 100T EC"},
    {"value": "heru_160t_ec", "label": "Heru 160T EC"},
    {"value": "heru_200t_ec", "label": "Heru 200T EC"},
    {"value": "heru_300t_ec", "label": "Heru 300T EC"},
]
