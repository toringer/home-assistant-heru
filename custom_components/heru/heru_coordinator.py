from datetime import timedelta
import logging
import async_timeout

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pymodbus.client import AsyncModbusTcpClient

from .const import DEFAULT_SLAVE, NAME

_LOGGER = logging.getLogger(__name__)


class HeruCoordinator(DataUpdateCoordinator):
    """HERU coordinator."""

    paused = False
    input_registers = {}
    holding_registers = []
    discrete_inputs = []
    coils = []

    def __init__(self, hass, client: AsyncModbusTcpClient):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=NAME,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=15),
        )
        self.client = client

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                if self.client.connected is False:
                    await self.client.connect()

                # 0x00001 - 0x00007
                coils_result = await self.client.read_coils(0, count=7, slave=DEFAULT_SLAVE)
                self.coils = coils_result.bits

                # 1x00001 - 1x00037
                discrete_inputs_result = await self.client.read_discrete_inputs(
                    0, count=54, slave=DEFAULT_SLAVE
                )
                self.discrete_inputs = discrete_inputs_result.bits

                # 3x00001 - 3x00034
                result = await self.client.read_input_registers(0, count=33, slave=DEFAULT_SLAVE)
                self.input_registers = {n: reg for n,reg in enumerate(result.registers)}
                # 3x00041 - 3x00046
                result = await self.client.read_input_registers(40, count=6, slave=DEFAULT_SLAVE)
                self.input_registers.update({n+40: reg for n,reg in enumerate(result.registers)})

                # 4x00001 - 4x00067
                holding_registers_result = await self.client.read_holding_registers(
                    0, count=69, slave=DEFAULT_SLAVE
                )
                self.holding_registers = holding_registers_result.registers

                return
        except Exception as err:
            raise UpdateFailed(f"Error communicating with unit: {err}")

    async def write_register(self, address: int, value: int):
        """Write to modbus register"""
        result = await self.client.write_register(address, value, slave=DEFAULT_SLAVE)
        await self.async_refresh()
        return result

    async def write_coil(self, address: int, value):
        """Write to modbus coil"""
        result = await self.client.write_coil(address, value, slave=DEFAULT_SLAVE)
        await self.async_refresh()
        return result

    def close(self):
        """Close client"""
        if self.client.connected is True:
            self.client.close()

    def pause(self):
        """Pause client"""
        self.paused = True
        if self.client.connected is True:
            self.client.close()

    async def resume(self):
        """Resume client"""
        self.paused = False
        return await self.client.connect()
