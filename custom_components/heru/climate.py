"""Support for Generic Modbus Thermostats."""
import logging
from typing import Any
from custom_components.heru.entity import HeruEntity

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from .const import (
    DOMAIN,
    HERU_CLIMATES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup climate platform."""
    _LOGGER.debug("HeruSensor.climate.py")
    coordinator = hass.data[DOMAIN]["coordinator"]

    climates = []
    for climate in HERU_CLIMATES:
        climates.append(HeruThermostat(coordinator, climate, entry))
    async_add_devices(climates)


class HeruThermostat(HeruEntity, ClimateEntity):
    """Representation of a Modbus Thermostat."""

    # https://developers.home-assistant.io/docs/core/entity/climate/

    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry) -> None:
        """Initialize the modbus thermostat."""
        _LOGGER.debug("HeruSensor.__init__()")
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx

        self._attr_min_temp = 15
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = PRECISION_WHOLE
        self._attr_hvac_mode = HVACMode.HEAT

        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()

    def _get_current_temperature(self):
        """Get the value from the coordinator"""
        return self.coordinator.input_registers[2] * 0.1

    def _get_target_temperature(self):
        """Get the value from the coordinator"""
        return self.coordinator.holding_registers[self.idx["address"]]

    def _get_hvac_action(self):
        action = self.coordinator.input_registers[28]
        if action == 0:
            return HVACAction.FAN
        else:
            return HVACAction.HEATING

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruThermostat._handle_coordinator_update()")
        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()

        _LOGGER.debug(
            "%s: %f %f",
            self._attr_name,
            self._attr_current_temperature,
            self._attr_target_temperature,
        )
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""

        _LOGGER.debug(
            "Mode: %s",
            hvac_mode,
        )
        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.write_coil(0, True)
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.write_coil(0, False)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""

        target_temperature = int(kwargs[ATTR_TEMPERATURE])
        _LOGGER.debug(
            "Set point: %s",
            target_temperature,
        )
        await self.coordinator.write_register(1, target_temperature)
