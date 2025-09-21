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

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry) -> None:
        """Initialize the modbus thermostat."""
        _LOGGER.debug("HeruSensor.__init__()")
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx
        self.modbus_address = self.idx["modbus_address"]

        self._attr_min_temp = 15
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._enable_turn_on_off_backwards_compatibility = False
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )

        self._attr_hvac_mode = self._get_hvac_mode()
        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()

    def _get_current_temperature(self):
        """Get the value from the coordinator"""
        # regulation_mode
        # - Mode 0 (Supply): Use supply air temperature (register 3x00003)
        # - Mode 1 (Extract): Use extract air temperature (register 3x00004)
        # - Mode 2 (Room): Use Room temperature (register 3x00008)
        # - Default: Fall back to supply air temperature
        regulation_mode = self.coordinator.get_register("4x00012")
        changeover = self.coordinator.get_register("3x00034")
        if regulation_mode == 0:  # Supply
            return self.coordinator.get_register("3x00003") * 0.1
        elif regulation_mode == 1:  # Extract
            return self.coordinator.get_register("3x00004") * 0.1
        elif regulation_mode == 2:  # Room
            return self.coordinator.get_register("3x00008") * 0.1
        elif regulation_mode == 3:  # Extract S/W
            if changeover == 1:
                return self.coordinator.get_register("3x00003") * 0.1  # Supply
            else:
                return self.coordinator.get_register("3x00004") * 0.1  # Extract
        elif regulation_mode == 4:  # Room S/W
            if changeover == 1:
                return self.coordinator.get_register("3x00003") * 0.1  # Supply
            else:
                return self.coordinator.get_register("3x00008") * 0.1  # Room
        else:
            return self.coordinator.get_register("3x00003") * 0.1  # Default to Supply

    def _get_target_temperature(self):
        """Get the value from the coordinator"""
        return self.coordinator.get_register(self.modbus_address)

    def _get_hvac_action(self):
        action = self.coordinator.get_register("3x00029")
        if action == 0:
            return HVACAction.FAN
        else:
            return HVACAction.HEATING

    def _get_hvac_mode(self):
        action = self.coordinator.get_register("0x00001")
        if action == False:
            return HVACMode.OFF
        else:
            return HVACMode.HEAT

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("HeruThermostat._handle_coordinator_update()")
        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()
        self._attr_hvac_mode = self._get_hvac_mode()

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
            await self.coordinator.write_coil_by_address("0x00001", True)
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.write_coil_by_address("0x00001", False)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self):
        """Turn the entity on."""
        _LOGGER.debug("Turn on")
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self):
        """Turn the entity off."""
        _LOGGER.debug("Turn off")
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""

        target_temperature = int(kwargs[ATTR_TEMPERATURE])
        _LOGGER.debug(
            "Set point: %s",
            target_temperature,
        )
        await self.coordinator.write_register_by_address("4x00002", target_temperature)
