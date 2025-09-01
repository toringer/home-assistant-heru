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


class HeruQualitySensor(HeruEntity, SensorEntity):
    """HeruQualitySensor class. Models the 3 possible quality sensors."""

    def __init__(self, coordinator: CoordinatorEntity, name, type_modbus_Address, value_modbus_Address, config_entry):
        _LOGGER.debug("HeruQualitySensor.__init__()")
        idx = {
            "name": name,
            "icon": None,
            "modbus_address": type_modbus_Address,
            "scale": 1.0,
            "state_class": SensorStateClass.MEASUREMENT,
            "entity_category": None,
            "register_type": INPUT_REGISTERS,
        }

        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.value_type = ModbusClientMixin.convert_from_registers(
            [coordinator.get_register(type_modbus_Address)],
            ModbusClientMixin.DATATYPE.INT16)
        self.idx = idx
        self.value_modbus_Address = value_modbus_Address
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_category = None
        self._attr_native_value = self._get_value()

        if self.value_type == 0:  # None
            self._attr_native_unit_of_measurement = None
            self._attr_entity_registry_enabled_default = False
        elif self.value_type == 1:  # RH
            self._attr_native_unit_of_measurement = "%"
            self._attr_device_class = SensorDeviceClass.HUMIDITY
            self._attr_entity_registry_enabled_default = True
        elif self.value_type == 2:  # CO2
            self._attr_native_unit_of_measurement = "ppm"
            self._attr_device_class = SensorDeviceClass.CO2
            self._attr_entity_registry_enabled_default = True
        elif self.value_type == 3:  # VOC
            self._attr_native_unit_of_measurement = "ppm"
            self._attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS
            self._attr_entity_registry_enabled_default = True
        else:
            raise TypeError(f"Unsupported value_type for sensor: {self.idx['name']}")

    def _get_value(self):
        """Get the value from the coordinator, but only if the sensor type matches configured."""

        configured_type = ModbusClientMixin.convert_from_registers(
            [self.coordinator.get_register(self.idx["modbus_address"])],
            ModbusClientMixin.DATATYPE.INT16)
        if self.value_type and configured_type == self.value_type:
            value = ModbusClientMixin.convert_from_registers(
                [self.coordinator.get_register(self.value_modbus_Address)],
                ModbusClientMixin.DATATYPE.INT16) * self.idx["scale"]
            return value
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruQualitySensor._handle_coordinator_update()")
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()
