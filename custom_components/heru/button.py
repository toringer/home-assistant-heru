"""Button platform for HERU."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import now as hass_now
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    BUTTON,
    DEFAULT_SLAVE,
    DOMAIN,
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
        HeruButtonSetTime("Sync date and time", None, entry, client),
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

    _attr_icon = "mdi:play-circle-outline"

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("HeruButtonStart.async_press()")
        result = await self._client.write_coil(self._address, True, DEFAULT_SLAVE)
        _LOGGER.debug("async_turn_on: %s", result)


class HeruButtonSetTime(HeruButton):
    """HERU start button class."""

    _attr_icon = "mdi:timer-sync"

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("HeruButtonSetTime.async_press()")

        now = hass_now()
        await self._client.write_register(399, now.year, DEFAULT_SLAVE)
        await self._client.write_register(400, now.month, DEFAULT_SLAVE)
        await self._client.write_register(401, now.day, DEFAULT_SLAVE)
        await self._client.write_register(402, now.hour, DEFAULT_SLAVE)
        await self._client.write_register(403, now.minute, DEFAULT_SLAVE)
        await self._client.write_register(404, now.second, DEFAULT_SLAVE)

        year_result = await self._client.read_holding_registers(399, 1, DEFAULT_SLAVE)
        month_result = await self._client.read_holding_registers(400, 1, DEFAULT_SLAVE)
        day_result = await self._client.read_holding_registers(401, 1, DEFAULT_SLAVE)
        hours_result = await self._client.read_holding_registers(402, 1, DEFAULT_SLAVE)
        minutes_result = await self._client.read_holding_registers(
            403, 1, DEFAULT_SLAVE
        )
        seconds_result = await self._client.read_holding_registers(
            404, 1, DEFAULT_SLAVE
        )
        _LOGGER.debug(
            "Date and time: %s-%s-%s %s.%s.%s",
            str(year_result.registers[0]),
            str(month_result.registers[0]),
            str(day_result.registers[0]),
            str(hours_result.registers[0]),
            str(minutes_result.registers[0]),
            str(seconds_result.registers[0]),
        )
