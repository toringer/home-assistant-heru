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
    _input_registers = {}
    _holding_registers = {}
    _discrete_inputs = {}
    _coils = {}

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

    def get_register(self, modbus_address: str):
        """Get register value by modbus address, automatically determining register type from prefix."""
        if modbus_address.startswith("0x"):
            return self._coils.get(modbus_address)
        elif modbus_address.startswith("1x"):
            return self._discrete_inputs.get(modbus_address)
        elif modbus_address.startswith("3x"):
            return self._input_registers.get(modbus_address)
        elif modbus_address.startswith("4x"):
            return self._holding_registers.get(modbus_address)
        else:
            raise ValueError(f"Invalid modbus address format: {modbus_address}. Must start with 0x, 1x, 3x, or 4x.")

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                if self.client.connected is False:
                    await self.client.connect()

                # Read coils efficiently - group consecutive addresses
                # 0x00001 - 0x00007 (addresses 0-6)
                coils_result = await self.client.read_coils(0, count=7, slave=DEFAULT_SLAVE)
                for i, bit in enumerate(coils_result.bits):
                    coil_address = f"0x{str(i + 1).zfill(5)}"
                    self._coils[coil_address] = bit

                # Read discrete inputs efficiently - group consecutive addresses
                # 1x00001 - 1x00054 (addresses 0-53)
                discrete_inputs_result = await self.client.read_discrete_inputs(
                    0, count=54, slave=DEFAULT_SLAVE
                )
                for i, bit in enumerate(discrete_inputs_result.bits):
                    discrete_address = f"1x{str(i + 1).zfill(5)}"
                    self._discrete_inputs[discrete_address] = bit

                # Read input registers efficiently - group consecutive addresses
                # 3x00001 - 3x00034 (addresses 0-33) - valid range
                result = await self.client.read_input_registers(0, count=34, slave=DEFAULT_SLAVE)
                for i, register in enumerate(result.registers):
                    input_address = f"3x{str(i + 1).zfill(5)}"
                    self._input_registers[input_address] = register

                # 3x00041 - 3x00046 (addresses 40-45) - valid range
                result = await self.client.read_input_registers(40, count=6, slave=DEFAULT_SLAVE)
                for i, register in enumerate(result.registers):
                    input_address = f"3x{str(40 + i + 1).zfill(5)}"
                    self._input_registers[input_address] = register

                # Read holding registers efficiently - group consecutive addresses
                # 4x00001 - 4x00067 (addresses 0-68)
                holding_registers_result = await self.client.read_holding_registers(
                    0, count=69, slave=DEFAULT_SLAVE
                )
                for i, register in enumerate(holding_registers_result.registers):
                    holding_address = f"4x{str(i + 1).zfill(5)}"
                    self._holding_registers[holding_address] = register

                return
        except Exception as err:
            raise UpdateFailed(f"Error communicating with unit: {err}")

    async def write_register_by_address(self, modbus_address: str, value: int):
        """Write to modbus register by modbus address (e.g., '4x00002')."""
        # Convert modbus_address (e.g., "4x00002") to numeric address (1)
        numeric_addr = int(modbus_address.replace("4x", "")) - 1
        result = await self.client.write_register(numeric_addr, value, slave=DEFAULT_SLAVE)
        await self.async_refresh()
        return result

    async def write_coil_by_address(self, modbus_address: str, value):
        """Write to modbus coil by modbus address (e.g., '0x00001')."""
        # Convert modbus_address (e.g., "0x00001") to numeric address (0)
        numeric_addr = int(modbus_address.replace("0x", "")) - 1
        result = await self.client.write_coil(numeric_addr, value, slave=DEFAULT_SLAVE)
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
