"""Support for Generic Modbus Thermostats."""
import logging

from typing import Any, cast

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
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DEFAULT_SLAVE,
    DOMAIN,
    CLIMATE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup climate platform."""
    _LOGGER.debug("HeruSensor.climate.py")

    client = hass.data[DOMAIN]["client"]

    climates = [HeruThermostat("HERU", client, config)]

    async_add_entities(climates, update_before_add=True)


class HeruThermostat(ClimateEntity):
    """Representation of a Modbus Thermostat."""

    # https://developers.home-assistant.io/docs/core/entity/climate/

    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(
        self,
        name: str,
        client: AsyncModbusTcpClient,
        config: dict[str, Any],
    ) -> None:
        """Initialize the modbus thermostat."""
        id_name = name.replace(" ", "").lower()
        self._attr_name = name
        self._attr_unique_id = ".".join([config.entry_id, CLIMATE, id_name])
        self._client = client

        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_mode = HVACMode.HEAT
        self._attr_precision = PRECISION_WHOLE
        self._attr_min_temp = 15
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""

        _LOGGER.debug(
            "Mode: %s",
            hvac_mode,
        )
        if hvac_mode == HVACMode.HEAT:
            await self._client.write_coil(0, True, DEFAULT_SLAVE)
        elif hvac_mode == HVACMode.OFF:
            await self._client.write_coil(0, False, DEFAULT_SLAVE)
        self._attr_hvac_mode = hvac_mode

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""

        target_temperature = int(kwargs[ATTR_TEMPERATURE])
        _LOGGER.debug(
            "Set point: %s",
            target_temperature,
        )
        await self._client.write_register(1, target_temperature, DEFAULT_SLAVE)
        await self.async_update()  # TODO hvor gjøres dette?

    async def async_update(self) -> None:
        """Update Target & Current Temperature."""
        current_temperature_result = await self._client.read_holding_registers(
            1, 1, DEFAULT_SLAVE
        )
        self._attr_target_temperature = current_temperature_result.registers[0]
        _LOGGER.debug(
            "Thermostat: %s",
            self._attr_target_temperature,
        )

        current_temperature_result = await self._client.read_input_registers(
            2, 1, DEFAULT_SLAVE
        )
        self._attr_current_temperature = current_temperature_result.registers[0] * 0.1

        current_heating_power_result = await self._client.read_input_registers(
            28, 1, DEFAULT_SLAVE
        )
        current_heating_power = current_heating_power_result.registers[0]
        _LOGGER.debug(
            "current_heating_power_result: %s",
            current_heating_power,
        )
        if current_heating_power == 0:
            self._attr_hvac_action = HVACAction.FAN
        else:
            self._attr_hvac_action = HVACAction.HEATING
