"""Sensor platform for HERU."""
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, EntityCategory, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import STATE_OFF
from homeassistant.const import STATE_ON
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from pymodbus.client.mixin import ModbusClientMixin

from custom_components.heru.HeruQualitySensor import HeruQualitySensor

from .const import (
    DISCRETE_INPUTS,
    DOMAIN,
    HERU_SENSORS,
    HOLDING_REGISTERS,
    INPUT_REGISTERS,
    INPUT_REGISTERS_BINARY,
)
from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices: AddEntitiesCallback
):
    """Setup sensor platform."""
    _LOGGER.debug("HeruSensor.sensor.py")
    coordinator = hass.data[DOMAIN]["coordinator"]

    sensors = []
    for sensor in HERU_SENSORS:
        sensors.append(HeruSensor(coordinator, sensor, entry))
    sensors.append(HeruLastSeenSensor(coordinator, entry))
    sensors.append(HeruRecycleEfficiencySensor(coordinator, entry))
    sensors.append(HeruQualitySensor(coordinator, "Quality sensor 1", "3x00041", "3x00042", entry))
    sensors.append(HeruQualitySensor(coordinator, "Quality sensor 2", "3x00043", "3x00044", entry))
    sensors.append(HeruQualitySensor(coordinator, "Quality sensor 3", "3x00045", "3x00046", entry))
    async_add_devices(sensors)


class HeruSensor(HeruEntity, SensorEntity):
    """HERU sensor class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("HeruSensor.__init__()")
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx

        self._attr_native_unit_of_measurement = self.idx["unit_of_measurement"]
        self._attr_device_class = self.idx["device_class"]
        if self._attr_device_class == SensorDeviceClass.ENUM:
            self._attr_options = self.idx["options"]
        self._attr_state_class = self.idx["state_class"]

        self._attr_entity_category = self.idx["entity_category"]
        self._attr_native_value = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        value = self.coordinator.get_register(self.idx["modbus_address"])

        if value is None:
            return None

        if self.idx["register_type"] == INPUT_REGISTERS:
            value = ModbusClientMixin.convert_from_registers([value], ModbusClientMixin.DATATYPE.INT16)

            if self._attr_device_class == SensorDeviceClass.ENUM:
                return self._attr_options[value]
            scaled_value = value * self.idx["scale"]
            if "precision" in self.idx and self.idx["precision"] is not None:
                return round(scaled_value, self.idx["precision"])
            return scaled_value
        if self.idx["register_type"] == INPUT_REGISTERS_BINARY:
            if value == 0:
                return STATE_OFF
            else:
                return STATE_ON
        if self.idx["register_type"] == DISCRETE_INPUTS:
            if value is False:
                return STATE_OFF
            else:
                return STATE_ON
        if self.idx["register_type"] == HOLDING_REGISTERS:
            if self._attr_device_class == SensorDeviceClass.ENUM:
                return self._attr_options[value]
            raise TypeError(f"Unsupported register type for sensor: {self.idx['name']}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruSensor._handle_coordinator_update()")
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()


class HeruLastSeenSensor(HeruEntity, SensorEntity):
    """HERU last seen sensor class."""

    def __init__(self, coordinator: CoordinatorEntity, config_entry):
        _LOGGER.debug("HeruLastSeenSensor.__init__()")
        idx = {
            "name": "Last seen",
            "device_class": SensorDeviceClass.TIMESTAMP,
            "icon": "mdi:clock",
            "modbus_address": "last_seen",
        }
        super().__init__(coordinator, idx, config_entry)
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_value = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        return dt_util.now(dt_util.DEFAULT_TIME_ZONE)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruLastSeenSensor._handle_coordinator_update()")
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()


class HeruRecycleEfficiencySensor(HeruEntity, SensorEntity):
    """HeruRecycleEfficiencySensor class."""

    def __init__(self, coordinator: CoordinatorEntity, config_entry):
        _LOGGER.debug("HeruRecycleEfficiencySensor.__init__()")
        idx = {
            "name": "Recycle efficiency",
            "icon": "mdi:recycle",
            "modbus_address": "recycle_efficiency",
        }
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_value = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        heat_recovery_temperature = ModbusClientMixin.convert_from_registers([self.coordinator.get_register("3x00007")], ModbusClientMixin.DATATYPE.INT16) * 0.1
        outdoor_temperature = ModbusClientMixin.convert_from_registers([self.coordinator.get_register("3x00002")], ModbusClientMixin.DATATYPE.INT16) * 0.1
        extract_air_temperature = ModbusClientMixin.convert_from_registers([self.coordinator.get_register("3x00004")], ModbusClientMixin.DATATYPE.INT16) * 0.1
        _LOGGER.debug(
            "Recycle efficiency: %s, %s, %s",
            heat_recovery_temperature,
            outdoor_temperature,
            extract_air_temperature,
        )
        try:
            factor = ((heat_recovery_temperature - outdoor_temperature) / (extract_air_temperature - outdoor_temperature)) * 100
            return round(factor, 2)
        except Exception:
            return 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruRecycleEfficiencySensor._handle_coordinator_update()")
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()
