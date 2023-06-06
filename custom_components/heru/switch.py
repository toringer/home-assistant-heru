"""Switch platform for HERU."""
import logging
from typing import Any
import datetime

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DEFAULT_SLAVE,
    DOMAIN,
    REGISTER_COILS,
    REGISTER_HOLDING,
    SWITCH,
)

from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(seconds=15)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices
):  # pylint: disable=unused-argument
    """Setup switch platform."""
    _LOGGER.debug("HERU.switch.py")
    client = hass.data[DOMAIN]["client"]

    switches = [
        HeruSwitchActive("Overpressure mode", 1, REGISTER_COILS, entry, client),
        HeruSwitchActive("Boost mode", 2, REGISTER_COILS, entry, client),
        HeruSwitchActive("Away mode", 3, REGISTER_COILS, entry, client),
        HeruSwitchActive("Preheater enabled", 63, REGISTER_HOLDING, entry, client),
        HeruSwitchActive("Heater enabled", 66, REGISTER_HOLDING, entry, client),
    ]

    async_add_devices(switches, update_before_add=True)


class HeruSwitch(HeruEntity, SwitchEntity):
    """HERU switch class."""

    _attr_icon = "mdi:toggle-switch-variant"

    def __init__(self, name: str, address: int, entry, hub: AsyncModbusTcpClient):
        _LOGGER.debug("HeruSwitch.__init__()")
        super().__init__(entry)
        self._hub = hub
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, str(address), SWITCH, id_name])


class HeruSwitchActive(HeruSwitch):
    """HERU active switch class."""

    def __init__(
        self,
        name: str,
        address: int,
        register_type,
        entry,
        client: AsyncModbusTcpClient,
    ):
        _LOGGER.debug("HeruSwitchActive.__init__()")
        super().__init__(name, address, entry, client)
        self._address = address
        self._client = client
        self._attr_name = name
        self._register_type = register_type
        self._skip_next_update = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        _LOGGER.debug("HeruSwitchActive.async_turn_on()")
        self._skip_next_update = True
        if self._register_type == REGISTER_COILS:
            result = await self._client.write_coil(self._address, True, DEFAULT_SLAVE)
        elif self._register_type == REGISTER_HOLDING:
            result = await self._client.write_register(self._address, 1, DEFAULT_SLAVE)
        else:
            raise Exception("register type '%s' not supported", self._register_type)
        _LOGGER.debug("async_turn_on: %s", result)
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        _LOGGER.debug("HeruSwitchActive.async_turn_off()")
        self._skip_next_update = True
        if self._register_type == REGISTER_COILS:
            result = await self._client.write_coil(self._address, False, DEFAULT_SLAVE)
        elif self._register_type == REGISTER_HOLDING:
            result = await self._client.write_register(self._address, 0, DEFAULT_SLAVE)
        else:
            raise Exception("register type '%s' not supported", self._register_type)
        _LOGGER.debug("async_turn_off: %s", result)
        self._attr_is_on = False

    async def async_update(self):
        """async_update"""
        if self._skip_next_update is True:
            self._skip_next_update = False
            _LOGGER.debug("%s: Skip update is active", self._attr_name)
            return

        if self._register_type == REGISTER_COILS:
            result = await self._client.read_coils(self._address, 1, DEFAULT_SLAVE)
            self._attr_is_on = result.bits[0]
        elif self._register_type == REGISTER_HOLDING:
            result = await self._client.read_holding_registers(
                self._address, 1, DEFAULT_SLAVE
            )
            self._attr_is_on = result.registers[0]
        else:
            raise Exception("register type '%s' not supported", self._register_type)
        _LOGGER.debug("%s: %s", self._attr_name, self._attr_is_on)
