"""Switch platform for HERU."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    COIL,
    DOMAIN,
    HERU_SWITCHES,
    HOLDING_REGISTERS,
)
from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices
):  # pylint: disable=unused-argument
    """Setup switch platform."""
    _LOGGER.debug("HERU.switch.py")

    coordinator = hass.data[DOMAIN]["coordinator"]
    switches = []
    for switch in HERU_SWITCHES:
        switches.append(HeruSwitch(coordinator, switch, entry))

    async_add_devices(switches)


class HeruSwitch(HeruEntity, SwitchEntity):
    """HERU switch class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, entry):
        _LOGGER.debug("HeruSwitch.__init__()")
        super().__init__(coordinator, idx, entry)
        self.idx = idx
        self.coordinator = coordinator
        self._attr_is_on = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator"""
        return self.coordinator.get_register(self.idx["modbus_address"])

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruSwitch._handle_coordinator_update()")
        self._attr_is_on = self._get_value()
        _LOGGER.debug(
            "%s: %s",
            self._attr_name,
            self._attr_is_on,
        )
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        _LOGGER.debug("HeruSwitch.async_turn_on()")
        if self.idx["register_type"] == COIL:
            result = await self.coordinator.write_coil_by_address(self.idx["modbus_address"], True)
        elif self.idx["register_type"] == HOLDING_REGISTERS:
            result = await self.coordinator.write_register_by_address(self.idx["modbus_address"], 1)
        _LOGGER.debug("async_turn_on: %s", result)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        _LOGGER.debug("HeruSwitch.async_turn_off()")
        if self.idx["register_type"] == COIL:
            result = await self.coordinator.write_coil_by_address(self.idx["modbus_address"], False)
        elif self.idx["register_type"] == HOLDING_REGISTERS:
            result = await self.coordinator.write_register_by_address(self.idx["modbus_address"], 0)
        _LOGGER.debug("async_turn_off: %s", result)
