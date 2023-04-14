"""Support for Generic Modbus Thermostats."""
import logging

from datetime import datetime
import struct
from typing import Any, cast

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_ADDRESS,
    CONF_NAME,
    CONF_TEMPERATURE_UNIT,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
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


class HeruThermostat(RestoreEntity, ClimateEntity):
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
        # super().__init__(config)
        id_name = name.replace(" ", "").lower()
        self._attr_name = name
        self._attr_unique_id = ".".join([config.entry_id, CLIMATE, id_name])
        self._client = client
        # self._target_temperature_register = config[CONF_TARGET_TEMP]
        # self._unit = config[CONF_TEMPERATURE_UNIT]

        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        # self._attr_hvac_mode = None
        self._attr_hvac_mode = HVACMode.HEAT
        # (
        #     UnitOfTemperature.FAHRENHEIT
        #     if self._unit == "F"
        #     else UnitOfTemperature.CELSIUS
        # )
        self._attr_precision = PRECISION_WHOLE
        # (
        #     PRECISION_TENTHS if self._precision >= 1 else PRECISION_WHOLE
        # )
        self._attr_min_temp = 15
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        # if CONF_HVAC_MODE_REGISTER in config:
        #     mode_config = config[CONF_HVAC_MODE_REGISTER]
        #     self._hvac_mode_register = mode_config[CONF_ADDRESS]
        #     self._attr_hvac_modes = cast(list[HVACMode], [])
        #     self._attr_hvac_mode = None
        #     self._hvac_mode_mapping: list[tuple[int, HVACMode]] = []
        #     self._hvac_mode_write_type = mode_config[CONF_WRITE_REGISTERS]
        #     mode_value_config = mode_config[CONF_HVAC_MODE_VALUES]

        #     for hvac_mode_kw, hvac_mode in (
        #         (CONF_HVAC_MODE_OFF, HVACMode.OFF),
        #         (CONF_HVAC_MODE_HEAT, HVACMode.HEAT),
        #         (CONF_HVAC_MODE_COOL, HVACMode.COOL),
        #         (CONF_HVAC_MODE_HEAT_COOL, HVACMode.HEAT_COOL),
        #         (CONF_HVAC_MODE_AUTO, HVACMode.AUTO),
        #         (CONF_HVAC_MODE_DRY, HVACMode.DRY),
        #         (CONF_HVAC_MODE_FAN_ONLY, HVACMode.FAN_ONLY),
        #     ):
        #         if hvac_mode_kw in mode_value_config:
        #             self._hvac_mode_mapping.append(
        #                 (mode_value_config[hvac_mode_kw], hvac_mode)
        #             )
        #             self._attr_hvac_modes.append(hvac_mode)

        # else:
        #     # No HVAC modes defined
        #     self._hvac_mode_register = None
        #     self._attr_hvac_mode = HVACMode.AUTO
        #     self._attr_hvac_modes = [HVACMode.AUTO]

        # if CONF_HVAC_ONOFF_REGISTER in config:
        #     self._hvac_onoff_register = config[CONF_HVAC_ONOFF_REGISTER]
        #     self._hvac_onoff_write_type = config[CONF_WRITE_REGISTERS]
        #     if HVACMode.OFF not in self._attr_hvac_modes:
        #         self._attr_hvac_modes.append(HVACMode.OFF)
        # else:
        #     self._hvac_onoff_register = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        # await self.async_base_added_to_hass()
        state = await self.async_get_last_state()
        if state and state.attributes.get(ATTR_TEMPERATURE):
            self._attr_target_temperature = float(state.attributes[ATTR_TEMPERATURE])

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""

        _LOGGER.debug(
            "Mode: %s",
            hvac_mode,
        )
        if hvac_mode == HVACMode.HEAT:
            result = await self._client.write_coil(0, True, 1)
        elif hvac_mode == HVACMode.OFF:
            result = await self._client.write_coil(0, False, 1)
        self._attr_hvac_mode = hvac_mode

        # if self._hvac_onoff_register is not None:
        #     # Turn HVAC Off by writing 0 to the On/Off register, or 1 otherwise.
        #     if self._hvac_onoff_write_type:
        #         await self._hub.async_pymodbus_call(
        #             self._slave,
        #             self._hvac_onoff_register,
        #             [0 if hvac_mode == HVACMode.OFF else 1],
        #             CALL_TYPE_WRITE_REGISTERS,
        #         )
        #     else:
        #         await self._hub.async_pymodbus_call(
        #             self._slave,
        #             self._hvac_onoff_register,
        #             0 if hvac_mode == HVACMode.OFF else 1,
        #             CALL_TYPE_WRITE_REGISTER,
        #         )

        # if self._hvac_mode_register is not None:
        #     # Write a value to the mode register for the desired mode.
        #     for value, mode in self._hvac_mode_mapping:
        #         if mode == hvac_mode:
        #             if self._hvac_mode_write_type:
        #                 await self._hub.async_pymodbus_call(
        #                     self._slave,
        #                     self._hvac_mode_register,
        #                     [value],
        #                     CALL_TYPE_WRITE_REGISTERS,
        #                 )
        #             else:
        #                 await self._hub.async_pymodbus_call(
        #                     self._slave,
        #                     self._hvac_mode_register,
        #                     value,
        #                     CALL_TYPE_WRITE_REGISTER,
        #                 )
        #             break

        # await self.async_update()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""

        target_temperature = int(kwargs[ATTR_TEMPERATURE])
        _LOGGER.debug(
            "Set point: %s",
            target_temperature,
        )
        await self._client.write_register(1, target_temperature, 1)
        # as_bytes = struct.pack(self._structure, target_temperature)
        # raw_regs = [
        #     int.from_bytes(as_bytes[i : i + 2], "big")
        #     for i in range(0, len(as_bytes), 2)
        # ]
        # registers = self._swap_registers(raw_regs)

        # if self._data_type in (
        #     DataType.INT16,
        #     DataType.UINT16,
        # ):
        #     result = await self._hub.async_pymodbus_call(
        #         self._slave,
        #         self._target_temperature_register,
        #         int(float(registers[0])),
        #         CALL_TYPE_WRITE_REGISTER,
        #     )
        # else:
        #     result = await self._hub.async_pymodbus_call(
        #         self._slave,
        #         self._target_temperature_register,
        #         [int(float(i)) for i in registers],
        #         CALL_TYPE_WRITE_REGISTERS,
        #     )
        # self._attr_available = result is not None
        await self.async_update()

    async def async_update(self) -> None:
        """Update Target & Current Temperature."""
        # remark "now" is a dummy parameter to avoid problems with
        # async_track_time_interval
        current_temperature_result = await self._client.read_holding_registers(1, 1, 1)
        self._attr_target_temperature = current_temperature_result.registers[0]
        _LOGGER.debug(
            "Thermostat: %s",
            self._attr_target_temperature,
        )

        current_temperature_result = await self._client.read_input_registers(2, 1, 1)
        self._attr_current_temperature = current_temperature_result.registers[0] * 0.1

        current_heating_power_result = await self._client.read_input_registers(28, 1, 1)
        current_heating_power = current_heating_power_result.registers[0]
        _LOGGER.debug(
            "current_heating_power_result: %s",
            current_heating_power,
        )
        if current_heating_power == 0:
            self._attr_hvac_action = HVACAction.FAN
        else:
            self._attr_hvac_action = HVACAction.HEATING

        # # do not allow multiple active calls to the same platform
        # if self._call_active:
        #     return
        # self._call_active = True
        # self._attr_target_temperature = await self._async_read_register(
        #     CALL_TYPE_REGISTER_HOLDING, self._target_temperature_register
        # )
        # self._attr_current_temperature = await self._async_read_register(
        #     self._input_type, self._address
        # )

        # # Read the mode register if defined
        # if self._hvac_mode_register is not None:
        #     hvac_mode = await self._async_read_register(
        #         CALL_TYPE_REGISTER_HOLDING, self._hvac_mode_register, raw=True
        #     )

        #     # Translate the value received
        #     if hvac_mode is not None:
        #         self._attr_hvac_mode = None
        #         for value, mode in self._hvac_mode_mapping:
        #             if hvac_mode == value:
        #                 self._attr_hvac_mode = mode
        #                 break

        # # Read th on/off register if defined. If the value in this
        # # register is "OFF", it will take precedence over the value
        # # in the mode register.
        # if self._hvac_onoff_register is not None:
        #     onoff = await self._async_read_register(
        #         CALL_TYPE_REGISTER_HOLDING, self._hvac_onoff_register, raw=True
        #     )
        #     if onoff == 0:
        #         self._attr_hvac_mode = HVACMode.OFF

        # self._call_active = False
        # self.async_write_ha_state()
