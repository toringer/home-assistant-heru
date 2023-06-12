"""Button platform for HERU."""
import logging

from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from .const import (
    DOMAIN,
    HERU_NUMBERS,
)
from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup number platform."""
    _LOGGER.debug("Heru.number.py")
    coordinator = hass.data[DOMAIN]["coordinator"]

    numbers = []
    for number in HERU_NUMBERS:
        numbers.append(HeruNumber(coordinator, number, entry))
    async_add_devices(numbers)


class HeruNumber(HeruEntity, NumberEntity):
    """HERU number class."""

    _attr_device_class = NumberDeviceClass.TEMPERATURE

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("HeruNumber.__init__()")
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.address = self.idx["address"]
        self.scale = self.idx["scale"]
        self._attr_native_value = 0
        self._attr_native_step = 1
        self._attr_native_min_value = idx["min_value"]
        self._attr_native_max_value = idx["max_value"]
        self._attr_native_unit_of_measurement = self.idx["unit_of_measurement"]
        self._attr_native_value = (
            self.coordinator.holding_registers[self.address] * self.scale
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruNumber._handle_coordinator_update()")
        self._attr_native_value = (
            self.coordinator.holding_registers[self.address] * self.scale
        )
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("HeruButton.async_set_native_value()")
        native_value = int(value / self.scale)
        await self.coordinator.write_register(self.address, native_value)
