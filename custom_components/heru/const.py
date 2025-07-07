"""Constants file"""

from homeassistant.const import Platform
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
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
ICON_COOLING = "mdi:snowflake"
ICON_HUMIDITY = "mdi:water-percent"

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
        "modbus_address": "3x00002",
        "address": 1,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Supply air temperature",
        "modbus_address": "3x00003",
        "address": 2,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Extract air temperature",
        "modbus_address": "3x00004",
        "address": 3,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Exhaust air temperature",
        "modbus_address": "3x00005",
        "address": 4,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Heat recovery temperature",
        "modbus_address": "3x00007",
        "address": 6,
        "scale": 0.1,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current exhaust fan power",
        "modbus_address": "3x00026",
        "address": 25,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current exhaust fan speed",
        "modbus_address": "3x00028",
        "address": 27,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "rpm",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current exhaust fan control voltage",
        "modbus_address": "3x00033",
        "address": 32,
        "scale": 0.1,
        "icon": ICON_FAN,
        "unit_of_measurement": "V",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current heating power",
        "modbus_address": "3x00029",
        "address": 28,
        "scale": 0.3921568627,
        "icon": ICON_HEAT_WAVE,
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current cooling power",
        "modbus_address": "3x00031",
        "address": 30,
        "scale": 0.3921568627,
        "icon": ICON_HEAT_WAVE,
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current supply fan power",
        "modbus_address": "3x00025",
        "address": 24,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current supply fan speed",
        "modbus_address": "3x00027",
        "address": 26,
        "scale": 1,
        "icon": ICON_FAN,
        "unit_of_measurement": "rpm",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current supply fan control voltage",
        "modbus_address": "3x00032",
        "address": 31,
        "scale": 0.1,
        "icon": ICON_FAN,
        "unit_of_measurement": "V",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Current heat/cold recovery power",
        "modbus_address": "3x00030",
        "address": 29,
        "scale": 0.3921568627,
        "icon": ICON_EXCHANGE,
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Night cooling active",
        "modbus_address": "1x00038",
        "address": 37,
        "scale": None,
        "icon": ICON_COOLING,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Filter timer alarm",
        "modbus_address": "1x00025",
        "address": 24,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Exhaust fan alarm",
        "modbus_address": "1x00022",
        "address": 21,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Boost input",
        "modbus_address": "1x00002",
        "address": 1,
        "scale": None,
        "icon": ICON_SWITCH,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Overpressure input",
        "modbus_address": "1x00003",
        "address": 2,
        "scale": None,
        "icon": ICON_SWITCH,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Fire alarm",
        "modbus_address": "1x00010",
        "address": 9,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Rotor alarm",
        "modbus_address": "1x00011",
        "address": 10,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Supply fan alarm",
        "modbus_address": "1x00021",
        "address": 20,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Current supply fan step",
        "modbus_address": "3x00023",
        "address": 22,
        "scale": None,
        "icon": ICON_FAN,
        "unit_of_measurement": None,
        "device_class": SensorDeviceClass.ENUM,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
        "options": ["Off", "Minimum", "Standard", "Maximum"],
    },
    {
        "name": "Current exhaust fan step",
        "modbus_address": "3x00024",
        "address": 23,
        "scale": None,
        "icon": ICON_FAN,
        "unit_of_measurement": None,
        "device_class": SensorDeviceClass.ENUM,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
        "options": ["Off", "Minimum", "Standard", "Maximum"],
    },
    {
        "name": "Filter days left",
        "modbus_address": "3x00020",
        "address": 19,
        "scale": 1,
        "icon": ICON_CALENDAR,
        "unit_of_measurement": "days",
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
    {
        "name": "Startup 1st phase",
        "modbus_address": "1x00028",
        "address": 27,
        "scale": None,
        "icon": ICON_START,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Startup 2nd phase",
        "modbus_address": "1x00029",
        "address": 28,
        "scale": None,
        "icon": ICON_START,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Cooling alarm",
        "modbus_address": "1x00032",
        "address": 31,
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Quality sensor 1 value",
        "modbus_address": "3x00042",
        "address": 41,
        "scale": 0.1,
        "icon": ICON_HUMIDITY,
        "unit_of_measurement": "%",
        "device_class": SensorDeviceClass.HUMIDITY,
        "state_class": SensorDeviceClass.MEASUREMENT,
        "entity_category": None,
        "register_type": INPUT_REGISTERS,
    },
]


HERU_NUMBERS = [
    {
        "name": "Night cooling indoor-outdoor diff. limit",
        "modbus_address": "4x00020",
        "address": 19,
        "scale": 0.1,
        "min_value": 1,
        "max_value": 10,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust high limit",
        "modbus_address": "4x00021",
        "address": 20,
        "scale": 1,
        "min_value": 18,
        "max_value": 24,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust low limit",
        "modbus_address": "4x00022",
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
        "modbus_address": "0x00005",
        "address": 4,
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Reset filter timer",
        "modbus_address": "0x00006",
        "address": 5,
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Sync date and time",
        "modbus_address": "4x00400",
        "address": 0,
        "icon": ICON_TIME_SYNC,
        "entity_class": BUTTON_CLASS_SET_TIME,
    },
]


HERU_SWITCHES = [
    {
        "name": "Power",
        "modbus_address": "0x00001",
        "address": 0,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Overpressure mode",
        "modbus_address": "0x00002",
        "address": 1,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Boost mode",
        "modbus_address": "0x00003",
        "address": 2,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Away mode",
        "modbus_address": "0x00004",
        "address": 3,
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Preheater enabled",
        "modbus_address": "4x00064",
        "address": 63,
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Heater enabled",
        "modbus_address": "4x00067",
        "address": 66,
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Night cooling enabled",
        "modbus_address": "4x00019",
        "address": 18,
        "icon": ICON_COOLING,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Cooler enabled",
        "modbus_address": "4x00069",
        "address": 68,
        "icon": ICON_COOLING,
        "register_type": HOLDING_REGISTERS,
    },
]


HERU_CLIMATES = [
    {
        "name": "Comfort",
        "modbus_address": "4x00002",
        "icon": ICON_THERMOSTAT,
        "address": 1,
    }
]
