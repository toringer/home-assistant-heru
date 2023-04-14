"""Switch platform for HERU."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.restore_state import RestoreEntity
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DOMAIN,
    SWITCH,
)

from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices
):  # pylint: disable=unused-argument
    """Setup switch platform."""
    _LOGGER.debug("HERU.switch.py")
    client = hass.data[DOMAIN]["client"]

    switches = [
        HeruSwitchActive("Unit on", 0, entry, client),
        HeruSwitchActive("Overpressure mode", 1, entry, client),
        HeruSwitchActive("Boost mode", 2, entry, client),
        HeruSwitchActive("Away mode", 3, entry, client),
    ]

    async_add_devices(switches, update_before_add=True)


# TODO hva er RestoreEntity?
class HeruSwitch(HeruEntity, SwitchEntity, RestoreEntity):
    """HERU switch class."""

    def __init__(self, name: str, address: int, entry, hub: AsyncModbusTcpClient):
        _LOGGER.debug("HeruSwitch.__init__()")
        super().__init__(entry)
        self._hub = hub
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, str(address), SWITCH, id_name])


class HeruSwitchActive(HeruSwitch):
    """HERU active switch class."""

    def __init__(self, name: str, address: int, entry, client: AsyncModbusTcpClient):
        _LOGGER.debug("HeruSwitchActive.__init__()")
        super().__init__(name, address, entry, client)
        self._address = address
        self._client = client
        self._attr_name = name

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        _LOGGER.debug("HeruSwitchActive.async_turn_on()")
        result = await self._client.write_coil(self._address, True, 1)
        _LOGGER.debug("async_turn_on: %s", result)
        # TODO valider modbus først
        # Hvis det kommer en update hvor HERU enda ikke rapporterer på så vil switch toggles av. Kanskje en liten hold her?
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        _LOGGER.debug("HeruSwitchActive.async_turn_off()")
        result = await self._client.write_coil(self._address, False, 1)
        _LOGGER.debug("async_turn_off: %s", result)
        # TODO valider modbus først
        self._attr_is_on = False

    async def async_update(self):
        """async_update"""
        result = await self._client.read_coils(self._address, 1, 1)
        self._attr_is_on = result.bits[0]
        _LOGGER.debug("%s: %s", self._attr_name, self._attr_is_on)
