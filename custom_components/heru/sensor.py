"""Sensor platform for HERU."""
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import STATE_OFF
from homeassistant.const import STATE_ON
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pymodbus.payload import BinaryPayloadDecoder, Endian

from .const import (
    DISCRETE_INPUTS,
    DOMAIN,
    HERU_SENSORS,
    INPUT_REGISTERS,
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

        self._attr_entity_category = self.idx["entity_category"]
        self._attr_native_value = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        if self.idx["register_type"] == INPUT_REGISTERS:
            value = self.coordinator.input_registers[self.idx["address"]]

            decorder = BinaryPayloadDecoder.fromRegisters([value], byteorder=Endian.BIG, wordorder=Endian.BIG)
            value = decorder.decode_16bit_int()

            if self._attr_device_class == SensorDeviceClass.ENUM:
                return self._attr_options[value]
            return value * self.idx["scale"]
        if self.idx["register_type"] == DISCRETE_INPUTS:
            value = self.coordinator.discrete_inputs[self.idx["address"]]
            if value is False:
                return STATE_OFF
            else:
                return STATE_ON

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
