"""Button platform for HERU."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    BUTTON,
    DOMAIN,
    ICON_START,
)

from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup button platform."""
    _LOGGER.debug("Heru.button.py")
    client = hass.data[DOMAIN]["client"]
    buttons = [
        HeruButtonStart("Clear Alarms", 4, entry, client),
        HeruButtonStart("Reset filter timer", 5, entry, client),
    ]

    async_add_devices(buttons)


class HeruButton(HeruEntity, ButtonEntity):
    """HERU button class."""

    def __init__(self, name: str, address: int, entry, client: AsyncModbusTcpClient):
        _LOGGER.debug("HeruButton.__init__()")
        super().__init__(entry)
        self._client = client
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, str(address), BUTTON, id_name])
        self._attr_name = name
        self._address = address
        _LOGGER.debug("self._attr_unique_id = %s", self._attr_unique_id)


class HeruButtonStart(HeruButton):
    """HERU start button class."""

    _attr_icon = ICON_START

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("HeruButtonStart.async_press()")
        result = await self._client.write_coil(self._address, True, 1)
        _LOGGER.debug("async_turn_on: %s", result)
