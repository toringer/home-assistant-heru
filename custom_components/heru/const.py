"""Constants file"""

from homeassistant.const import Platform
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
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
ICON_THERMOMETER_LINES = "mdi:thermometer-lines"
ICON_AIR_PURIFIER = "mdi:air-purifier"

# Platforms
SENSOR = Platform.SENSOR
SWITCH = Platform.SWITCH
BUTTON = Platform.BUTTON
NUMBER = Platform.NUMBER
SELECT = Platform.SELECT
CLIMATE = Platform.CLIMATE
BINARY_SENSOR = Platform.BINARY_SENSOR
PLATFORMS = [SENSOR, SWITCH, BUTTON, CLIMATE, NUMBER, BINARY_SENSOR]
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
INPUT_REGISTERS_BINARY = "input_registers_binary"
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
        "scale": None,
        "icon": ICON_ALARM,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "register_type": DISCRETE_INPUTS,
    },
    {
        "name": "Temperature regulation mode",
        "modbus_address": "4x00012",
        "scale": None,
        "icon": ICON_THERMOMETER_LINES,
        "unit_of_measurement": None,
        "device_class": SensorDeviceClass.ENUM,
        "state_class": None,
        "entity_category": None,
        "register_type": HOLDING_REGISTERS,
        "options": ["Supply", "Extract", "Room", "Extract S/W", "Room S/W"],
    },
    {
        "name": "Changeover active",
        "modbus_address": "3x00034",
        "scale": None,
        "icon": ICON_CALENDAR,
        "unit_of_measurement": None,
        "device_class": None,
        "state_class": None,
        "entity_category": None,
        "register_type": INPUT_REGISTERS_BINARY,
    },
]


HERU_BINARY_SENSORS = [
    #     {
    #     "name": "NAME",
    #     "modbus_address": "9x99999",
    #     "icon": ICON,
    #     "device_class": BinarySensorDeviceClass.RUNNING,
    #     "entity_category": EntityCategory.DIAGNOSTIC,
    #     "register_type": DISCRETE_INPUTS,
    # },
]


HERU_NUMBERS = [
    {
        "name": "Night cooling indoor-outdoor diff. limit",
        "modbus_address": "4x00020",
        "scale": 0.1,
        "min_value": 1,
        "max_value": 10,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust high limit",
        "modbus_address": "4x00021",
        "scale": 1,
        "min_value": 18,
        "max_value": 24,
        "icon": ICON_THERMOMETER,
        "unit_of_measurement": "°C",
    },
    {
        "name": "Night cooling exhaust low limit",
        "modbus_address": "4x00022",
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
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Reset filter timer",
        "modbus_address": "0x00006",
        "icon": ICON_PLAY,
        "entity_class": BUTTON_CLASS_START,
    },
    {
        "name": "Sync date and time",
        "modbus_address": "4x00400",
        "icon": ICON_TIME_SYNC,
        "entity_class": BUTTON_CLASS_SET_TIME,
    },
]


HERU_SWITCHES = [
    {
        "name": "Power",
        "modbus_address": "0x00001",
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Overpressure mode",
        "modbus_address": "0x00002",
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Boost mode",
        "modbus_address": "0x00003",
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Away mode",
        "modbus_address": "0x00004",
        "icon": ICON_SWITCH,
        "register_type": COIL,
    },
    {
        "name": "Preheater enabled",
        "modbus_address": "4x00064",
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Heater enabled",
        "modbus_address": "4x00067",
        "icon": ICON_SWITCH,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Night cooling enabled",
        "modbus_address": "4x00019",
        "icon": ICON_COOLING,
        "register_type": HOLDING_REGISTERS,
    },
    {
        "name": "Cooler enabled",
        "modbus_address": "4x00069",
        "icon": ICON_COOLING,
        "register_type": HOLDING_REGISTERS,
    },
]


HERU_CLIMATES = [
    {
        "name": "Comfort",
        "modbus_address": "4x00002",
        "icon": ICON_THERMOSTAT,
    }
]
