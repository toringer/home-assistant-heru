"""Binary Sensor platform for HERU."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DISCRETE_INPUTS,
    DOMAIN,
    HERU_SENSORS,
)
from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices: AddEntitiesCallback
):
    """Setup binary sensor platform."""
    _LOGGER.debug("HeruBinarySensor.binary_sensor.py")
    coordinator = hass.data[DOMAIN]["coordinator"]

    binary_sensors = []
    for sensor in HERU_SENSORS:
        if sensor["register_type"] == DISCRETE_INPUTS:
            binary_sensors.append(HeruBinarySensor(coordinator, sensor, entry))

    if binary_sensors:
        async_add_devices(binary_sensors)


class HeruBinarySensor(HeruEntity, BinarySensorEntity):
    """HERU binary sensor class for discrete inputs."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("HeruBinarySensor.__init__()")
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx
        self.name = self.idx["name"]
        self.modbus_address = self.idx["modbus_address"]
        self.register_type = self.idx["register_type"]

        # Set device class based on the sensor name/type
        if "alarm" in self.name.lower():
            self._attr_device_class = BinarySensorDeviceClass.PROBLEM
        elif "fan" in self.name.lower():
            self._attr_device_class = BinarySensorDeviceClass.RUNNING
        elif "cooling" in self.name.lower():
            self._attr_device_class = BinarySensorDeviceClass.COLD
        elif "startup" in self.name.lower():
            self._attr_device_class = BinarySensorDeviceClass.RUNNING
        else:
            self._attr_device_class = None

        self._attr_entity_category = self.idx["entity_category"]
        self._attr_is_on = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        if self.register_type == DISCRETE_INPUTS:
            value = self.coordinator.get_register(self.modbus_address)
            return bool(value)
        return False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruBinarySensor._handle_coordinator_update()")
        self._attr_is_on = self._get_value()
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_is_on,
        )
        self.async_write_ha_state()
