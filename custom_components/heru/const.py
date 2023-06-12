"""Constants file"""

from homeassistant.const import Platform
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

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
ICON_THERMOMETER = "mdi:thermometer"
ICON_SWITCH = "mdi:toggle-switch-variant"
ICON_PLAY = "mdi:play-circle-outline"
ICON_TIME_SYNC = "mdi:timer-sync"
ICON_CALENDAR = "mdi:calendar"
ICON_THERMOSTAT = "mdi:home-thermometer"
ICON_START = "mdi:ray-start-arrow"

# Platforms
SENSOR = Platform.SENSOR
SWITCH = Platform.SWITCH
BUTTON = Platform.BUTTON
NUMBER = Platform.NUMBER
SELECT = Platform.SELECT
CLIMATE = Platform.CLIMATE
PLATFORMS = [SENSOR, SWITCH, BUTTON, CLIMATE, NUMBER]
# PLATFORMS = [SWITCH, SENSOR, BUTTON, NUMBER, SELECT]

# Modbus
DEFAULT_SLAVE = 1
REGISTER_HOLDING = "holding"
REGISTER_COILS = "coils"

# Configuration and options
CONF_HOST_NAME = "host_name"
CONF_HOST_PORT = "host_port"
CONF_DEVICE_NAME = "device_name"

# Modbus register types
INPUT_REGISTERS = "input_registers"
DISCRETE_INPUTS = "discrete_inputs"
HOLDING_REGISTERS = "holding_registers"
COIL = "coil"

#  Button class types
BUTTON_CLASS_START = "button_class_start"
BUTTON_CLASS_SET_TIME = "button_class_set_time"


HERU_SENSORS = [
    {
        "name": "Outdoor temperature",
        "address": 1,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Supply air temperature",
        "address": 2,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Extract air temperature",
        "address": 3,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Exhaust air temperature",
        "address": 4,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Heat recovery temperature",
        "address": 6,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current exhaust fan power",
        "address": 25,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "%",
        "device_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current heating power",
        "address": 28,
        "scale": 0.3921568627,
        "icon": ICON_HEAT_WAVE,
        "unit_of_measurement": "%",
        "device_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current supply fan power",
        "address": 24,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "%",
        "device_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current heat/cold recovery power",
        "address": 29,
        "scale": 0.3921568627,
        "icon": ICON_EXCHANGE,
        "unit_of_measurement": "%",
        "device_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Night cooling active",
        "address": 37,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Filter timer alarm",
        "address": 24,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Exhaust fan alarm",
        "address": 21,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Boost input",
        "address": 1,
        "scale": None,
        "icon": ICON_SWITCH,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": None,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Overpressure input",
        "address": 2,
        "scale": None,
        "icon": ICON_SWITCH,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": None,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Fire alarm",
        "address": 9,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Rotor alarm",
        "address": 10,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Supply fan alarm",
        "address": 20,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Current supply fan step",
        "address": 22,
        "scale": None,
        "icon": ICON_FAN,
        "unit_of_measurement": None,
        "device_class": SensorDeviceClass.ENUM,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
        "options": ["Off", "Minimum", "Standard", "Maximum"],
    },
    {
        "name": "Current exhaust fan step",
        "address": 23,
        "scale": None,
        "icon": ICON_FAN,
        "unit_of_measurement": None,
        "device_class": SensorDeviceClass.ENUM,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
        "options": ["Off", "Minimum", "Standard", "Maximum"],
    },
    {
        "name": "Filter days left",
        "address": 19,
        "scale": 1,
        "icon": ICON_CALENDAR,
        "unit_of_measurement": "days",
        "device_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Startup 1st phase",
        "address": 27,
        "scale": None,
        "icon": ICON_START,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Startup 2nd phase",
        "address": 28,
        "scale": None,
        "icon": ICON_START,
        "unit_of_measurement": None,
        "device_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
]


HERU_NUMBERS = [
    {
        "name": "Night cooling indoor-outdoor diff. limit",
        "address": 19,
        "scale": 0.1,
        "min_value": 1,
        "max_value": 10,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust high limit",
        "address": 20,
        "scale": 1,
        "min_value": 18,
        "max_value": 24,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust low limit",
        "address": 21,
        "scale": 1,
        "min_value": 19,
        "max_value": 26,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
]


HERU_BUTTONS = [
    {
        "name": "Clear Alarms",
        "address": 4,
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Reset filter timer",
        "address": 5,
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Sync date and time",
        "address": 0,
        "icon": ICON_TIME_SYNC,
        "entity_class": BUTTON_CLASS_SET_TIME,
    },
]


HERU_SWITCHES = [
    {
        "name": "Overpressure mode",
        "address": 1,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Boost mode",
        "address": 2,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Away mode",
        "address": 3,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Preheater enabled",
        "address": 63,
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Heater enabled",
        "address": 66,
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Night cooling enabled",
        "address": 18,
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
]


HERU_CLIMATES = [
    {
        "name": "Comfort",
        "icon": ICON_THERMOSTAT,
        "address": 1,
    }
]
