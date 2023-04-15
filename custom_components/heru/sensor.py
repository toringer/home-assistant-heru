"""Sensor platform for HERU."""
import logging


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_OFF
from homeassistant.const import STATE_ON
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from datetime import datetime
import pytz
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DOMAIN,
    SENSOR,
)
from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices: AddEntitiesCallback
):
    """Setup sensor platform."""
    _LOGGER.debug("HeruSensor.sensor.py")

    client = hass.data[DOMAIN]["client"]

    # Address input = Spec. address - 1
    sensors = [
        HeruTemperatureSensor("Outdoor temperature", 1, True, 0.1, client, entry),
        HeruTemperatureSensor("Supply air temperature", 2, True, 0.1, client, entry),
        HeruTemperatureSensor("Extract air temperature", 3, True, 0.1, client, entry),
        HeruTemperatureSensor("Exhaust air temperature", 4, True, 0.1, client, entry),
        HeruTemperatureSensor("Water temperature", 5, False, 1, client, entry),
        HeruTemperatureSensor("Heat recovery temperature", 6, True, 0.1, client, entry),
        HeruTemperatureSensor("Room temperature", 7, False, 1, client, entry),
        HeruTemperatureSensor(
            "Supply pressure - duct (GP1)", 11, False, 10, client, entry
        ),
        HeruDaySensor("Filter days left", 19, False, client, entry),
        HeruEnumSensor("Current supply fan step", 22, False, client, entry),
        HeruAlarmSensor("Fire alarm", 9, True, client, entry),
        HeruAlarmSensor("Rotor alarm", 10, True, client, entry),
        HeruAlarmSensor("Filter timer alarm", 24, True, client, entry),
        HeruNumberSensor(
            "Current heating power", 28, True, 0.3921568627, client, entry
        ),
    ]

    # now = datetime.now(pytz.timezone("Europe/Oslo"))  # TODO
    # # await client.write_coil(399, now.year, 1)
    # # await client.write_coil(400, now.month, 1)
    # # await client.write_coil(401, now.day, 1)
    # # await client.write_coil(402, now.hour, 1)
    # await client.write_coil(403, now.minute, 1)
    # # await client.write_coil(404, now.second, 1)
    # _LOGGER.debug("Now: %s", str(now.minute))
    # # await self._client.write_coil(self._address, True, 1)

    async_add_devices(sensors, update_before_add=True)


class HeruSensor(HeruEntity, SensorEntity):
    """HERU sensor class."""

    def __init__(self, name: str, address: int, client: AsyncModbusTcpClient, entry):
        _LOGGER.debug("HeruSensor.__init__()")
        super().__init__(entry)
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, SENSOR, id_name])
        self._attr_name = name
        self._address = address
        self._client = client


class HeruTemperatureSensor(HeruSensor):
    """HERU sensor class."""

    _attr_native_unit_of_measurement = "°C"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_icon = "mdi:thermometer"

    def __init__(
        self,
        name: str,
        address: int,
        enabled: bool,
        scale: float,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruTemperatureSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._scale = scale
        self._attr_unique_id = ".".join(
            [entry.entry_id, str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = 0
        self._client = client
        self._attr_entity_registry_enabled_default = True  # TODO enabled

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(self._address, 1, 1)
        self._attr_native_value = result.registers[0] * self._scale
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )


class HeruDaySensor(HeruSensor):
    """HERU sensor class."""

    _attr_native_unit_of_measurement = "days"
    _attr_icon = "mdi:calendar"

    def __init__(
        self,
        name: str,
        address: int,
        enabled: bool,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruTemperatureSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._attr_unique_id = ".".join(
            [entry.entry_id, str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = 0
        self._client = client
        self._attr_entity_registry_enabled_default = True  # TODO enabled

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(self._address, 1, 1)
        self._attr_native_value = result.registers[0]
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )


class HeruNumberSensor(HeruSensor):
    """HERU sensor class."""

    _attr_native_unit_of_measurement = "%"
    _attr_icon = "mdi:heat-wave"

    def __init__(
        self,
        name: str,
        address: int,
        enabled: bool,
        scale: float,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruTemperatureSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._attr_unique_id = ".".join(
            [entry.entry_id, str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = 0
        self._client = client
        self._scale = scale
        self._attr_entity_registry_enabled_default = True  # TODO enabled

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(self._address, 1, 1)
        self._attr_native_value = round(result.registers[0] * self._scale, 1)
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_native_value,
        )


class HeruEnumSensor(HeruSensor):
    """HERU sensor class."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:thermometer"

    def __init__(
        self,
        name: str,
        address: int,
        enabled: bool,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruTemperatureSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._attr_unique_id = ".".join(
            [entry.entry_id, str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = 0
        self._client = client
        self._attr_entity_registry_enabled_default = True  # TODO enabled
        self._attr_options = ["Off", "Minimum", "Standard", "Maximum"]

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(self._address, 1, 1)
        if result.registers[0] == 0:
            self._attr_native_value = "Off"
        elif result.registers[0] == 1:
            self._attr_native_value = "Minimum"
        elif result.registers[0] == 2:
            self._attr_native_value = "Standard"
        elif result.registers[0] == 3:
            self._attr_native_value = "Maximum"
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_native_value,
        )


class HeruAlarmSensor(HeruSensor):
    """HERU sensor class."""

    # _attr_native_unit_of_measurement = "°C"
    _attr_state_class = None
    # _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_icon = "mdi:bell"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        name: str,
        address: int,
        enabled: bool,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruTemperatureSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._attr_unique_id = ".".join(
            [entry.entry_id, str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = STATE_OFF

        self._client = client
        self._attr_entity_registry_enabled_default = True  # TODO enabled

    async def async_update(self):
        """async_update"""
        result = await self._client.read_discrete_inputs(self._address, 1, 1)
        if result.bits[0] is False:
            self._attr_native_value = STATE_OFF
        else:
            self._attr_native_value = STATE_ON
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_native_value,
        )
