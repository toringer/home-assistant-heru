"""Sensor platform for HERU."""
import logging
import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
    RestoreSensor,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .helpers.general import get_parameter

from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DEFAULT_SLAVE,
    DOMAIN,
    CONF_DEVICE_NAME,
    CONF_DEVICE_MODEL,
    DEVICE_CONSUMPTION,
    ICON_ALARM,
    ICON_EXCHANGE,
    ICON_FAN,
    ICON_HEAT_WAVE,
    ICON_SWITCH,
    ICON_ENERGY,
    SENSOR,
)

from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(seconds=15)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices: AddEntitiesCallback
):
    """Setup sensor platform."""
    _LOGGER.debug("HeruSensor.sensor.py")

    client = hass.data[DOMAIN]["client"]

    # Address input = Spec. address - 1
    sensors = [
        HeruTemperatureSensor("Outdoor temperature", 1, 0.1, client, entry),
        HeruTemperatureSensor("Supply air temperature", 2, 0.1, client, entry),
        HeruTemperatureSensor("Extract air temperature", 3, 0.1, client, entry),
        HeruTemperatureSensor("Exhaust air temperature", 4, 0.1, client, entry),
        HeruTemperatureSensor("Heat recovery temperature", 6, 0.1, client, entry),
        HeruDaySensor("Filter days left", 19, client, entry),
        HeruEnumSensor("Current supply fan step", ICON_FAN, 22, client, entry),
        HeruEnumSensor("Current exhaust fan step", ICON_FAN, 23, client, entry),
        HeruAlarmSensor("Boost input", ICON_SWITCH, None, 1, client, entry),
        HeruAlarmSensor("Overpressure input", ICON_SWITCH, None, 2, client, entry),
        HeruAlarmSensor(
            "Fire alarm", ICON_ALARM, EntityCategory.DIAGNOSTIC, 9, client, entry
        ),
        HeruAlarmSensor(
            "Rotor alarm", ICON_ALARM, EntityCategory.DIAGNOSTIC, 10, client, entry
        ),
        HeruAlarmSensor(
            "Supply fan alarm", ICON_ALARM, EntityCategory.DIAGNOSTIC, 20, client, entry
        ),
        HeruAlarmSensor(
            "Exhaust fan alarm",
            ICON_ALARM,
            EntityCategory.DIAGNOSTIC,
            21,
            client,
            entry,
        ),
        HeruAlarmSensor(
            "Filter timer alarm",
            ICON_ALARM,
            EntityCategory.DIAGNOSTIC,
            24,
            client,
            entry,
        ),
        HeruNumberSensor(
            "Current heating power",
            ICON_HEAT_WAVE,
            28,
            0.3921568627,
            client,
            entry,
        ),
        HeruNumberSensor(
            "Current supply fan power",
            ICON_FAN,
            24,
            1,
            client,
            entry,
        ),
        HeruNumberSensor(
            "Current heat/cold recovery power",
            ICON_EXCHANGE,
            29,
            0.3921568627,
            client,
            entry,
        ),
        HeruNumberSensor("Current exhaust fan power", ICON_FAN, 25, 1, client, entry),
    ]

    # If device model not selected, do not add those sensors
    if get_parameter(entry, CONF_DEVICE_MODEL) is not None:
        sensors.extend(
            [
                HeruPowerSensor("Instantaneous power", entry),
                HeruEnergySensor("Energy consumption", entry),
            ]
        )
    async_add_devices(sensors, update_before_add=True)


class HeruPowerSensor(HeruEntity, SensorEntity):
    """Heru Power Sensor class."""

    _attr_native_unit_of_measurement = "W"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.POWER

    def __init__(self, name: str, entry):
        _LOGGER.debug("HeruPowerSensor.__init__()")
        super().__init__(entry)
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, SENSOR, id_name])
        self._attr_name = name
        self._attr_icon = ICON_ENERGY
        self._device_name = entry.data[CONF_DEVICE_NAME]
        self._device_model = get_parameter(entry, CONF_DEVICE_MODEL)
        self._heater_p_entity = (
            "sensor." + self._device_name.lower() + "_current_heating_power"
        )
        self._supply_p_entity = (
            "sensor." + self._device_name.lower() + "_current_supply_fan_power"
        )
        self._exhaust_p_entity = (
            "sensor." + self._device_name.lower() + "_current_exhaust_fan_power"
        )
        self._attr_should_poll = False  # Disable polling
        self._state = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        async_track_state_change_event(
            self.hass,
            [self._heater_p_entity, self._supply_p_entity, self._exhaust_p_entity],
            self.schedule_update_ha_state,
        )

    async def async_update(self):
        """async_update"""

        if all(
            entity in self.hass.states._states.keys()
            for entity in [
                self._heater_p_entity,
                self._supply_p_entity,
                self._exhaust_p_entity,
            ]
        ):
            heater_p = float(self.hass.states.get(self._heater_p_entity).state)
            supply_p = float(self.hass.states.get(self._supply_p_entity).state)
            exhaust_p = float(self.hass.states.get(self._exhaust_p_entity).state)
            self._attr_native_value = (
                DEVICE_CONSUMPTION[self._device_model]["heater_p"] * heater_p / 100
                + DEVICE_CONSUMPTION[self._device_model]["fans_p"] / 2 * supply_p / 100
                + DEVICE_CONSUMPTION[self._device_model]["fans_p"] / 2 * exhaust_p / 100
                + DEVICE_CONSUMPTION[self._device_model]["board_p"]
            )
            _LOGGER.debug(
                "%s: %s %s",
                self._attr_name,
                self._attr_native_value,
                self._attr_native_unit_of_measurement,
            )


class HeruEnergySensor(HeruEntity, RestoreSensor):
    """Heru Power Sensor class."""

    _attr_native_unit_of_measurement = "Wh"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, name: str, entry):
        _LOGGER.debug("HeruPowerSensor.__init__()")
        super().__init__(entry)
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, SENSOR, id_name])
        self._attr_name = name
        self._attr_icon = ICON_ENERGY
        self._device_name = entry.data[CONF_DEVICE_NAME]
        self._device_model = entry.data[CONF_DEVICE_MODEL]
        self._power_entity = (
            "sensor." + self._device_name.lower() + "_instantaneous_power"
        )
        self.entity_id = "sensor." + self._device_name.lower() + "_energy_consumption"
        self._state = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            # new introduced in 2022.04
            if last_sensor_data.native_value is None:
                self._state = 0
            else:
                self._state = last_sensor_data.native_value

    async def async_update(self):
        """async_update"""

        if all(
            entity in self.hass.states._states.keys()
            for entity in [self._power_entity, self.entity_id]
        ):
            if self.hass.states.get(self._power_entity).state != "unknown":
                self._state = (
                    float(self.hass.states.get(self._power_entity).state)
                    * SCAN_INTERVAL.total_seconds()
                    / 3600
                    + self._state
                )
            self._attr_native_value = self._state
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )


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

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(
            self._address, 1, DEFAULT_SLAVE
        )
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

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(
            self._address, 1, DEFAULT_SLAVE
        )
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

    def __init__(
        self,
        name: str,
        icon: str,
        address: int,
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
        self._attr_icon = icon

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(
            self._address, 1, DEFAULT_SLAVE
        )
        self._attr_native_value = round(
            result.registers[0] * self._scale, DEFAULT_SLAVE
        )
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_native_value,
        )


class HeruEnumSensor(HeruSensor):
    """HERU sensor class."""

    _attr_device_class = SensorDeviceClass.ENUM

    def __init__(
        self,
        name: str,
        icon: str,
        address: int,
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
        self._attr_icon = icon
        self._attr_options = ["Off", "Minimum", "Standard", "Maximum"]

    async def async_update(self):
        """async_update"""
        result = await self._client.read_input_registers(
            self._address, 1, DEFAULT_SLAVE
        )
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

    _attr_state_class = None

    def __init__(
        self,
        name: str,
        icon: str,
        category: EntityCategory,
        address: int,
        client: AsyncModbusTcpClient,
        entry,
    ):
        _LOGGER.debug("HeruAlarmSensor.__init__()")
        super().__init__(name, address, client, entry)
        self._attr_unique_id = ".".join(
            [entry.entry_id, "alarm", str(address), SENSOR]
        )  # TODO Kan denne flyttes til base?.
        self._attr_native_value = STATE_OFF
        self._attr_icon = icon
        self._attr_entity_category = category
        self._client = client

    async def async_update(self):
        """async_update"""
        result = await self._client.read_discrete_inputs(
            self._address, 1, DEFAULT_SLAVE
        )
        if result.bits[0] is False:
            self._attr_native_value = STATE_OFF
        else:
            self._attr_native_value = STATE_ON
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_native_value,
        )
