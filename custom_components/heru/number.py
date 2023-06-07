"""Button platform for HERU."""
import logging
import datetime

from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.core import HomeAssistant
from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    DEFAULT_SLAVE,
    DOMAIN,
    ICON_THERMOMETER,
    NUMBER,
)

from .entity import HeruEntity

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(seconds=15)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup number platform."""
    _LOGGER.debug("Heru.number.py")
    client = hass.data[DOMAIN]["client"]
    numbers = [
        HeruNumber(
            "Night cooling indoor-outdoor diff. limit", 1, 10, 0.1, 19, entry, client
        ),
        HeruNumber("Night cooling exhaust high limit", 18, 24, 1, 20, entry, client),
        HeruNumber("Night cooling exhaust low limit", 19, 26, 1, 21, entry, client),
    ]

    async_add_devices(numbers, update_before_add=True)


class HeruNumber(HeruEntity, NumberEntity):
    """HERU button class."""

    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_icon = ICON_THERMOMETER

    def __init__(
        self,
        name: str,
        min_value: float,
        max_value: float,
        scale: float,
        address: int,
        entry,
        client: AsyncModbusTcpClient,
    ):
        _LOGGER.debug("HeruNumber.__init__()")
        super().__init__(entry)
        self._client = client
        id_name = name.replace(" ", "").lower()
        self._attr_unique_id = ".".join([entry.entry_id, str(address), NUMBER, id_name])
        self._attr_name = name
        self._address = address
        self._scale = scale
        self._attr_native_unit_of_measurement = "°C"
        self._attr_native_value = 0
        self._attr_native_step = 1
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value

    async def async_update(self):
        """async_update"""
        result = await self._client.read_holding_registers(
            self._address, 1, DEFAULT_SLAVE
        )
        self._attr_native_value = result.registers[0] * self._scale
        _LOGGER.debug(
            "%s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("HeruButton.async_set_native_value()")
        native_value = int(value / self._scale)
        await self._client.write_register(self._address, native_value, DEFAULT_SLAVE)
