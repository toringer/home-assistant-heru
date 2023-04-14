"""Helpers for config_flow"""

from collections import UserDict
import logging
from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as async_device_registry_get
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.helpers.entity_registry import async_get as async_entity_registry_get
from homeassistant.helpers.entity_registry import (
    EntityRegistry,
    RegistryEntry,
)


# pylint: disable=relative-beyond-top-level
from ..const import (
    CONF_HOST_PORT,
    CONF_DEVICE_NAME,
    CONF_HOST_NAME,
    DOMAIN,
    NAME,
    SWITCH,
)
from pymodbus.client import (
    AsyncModbusTcpClient,
)

_LOGGER = logging.getLogger(__name__)


class FlowValidator:
    """Validator of flows"""

    @staticmethod
    async def validate_step_user(
        hass: HomeAssistant, user_input: dict[str, Any]
    ) -> list[str]:
        """Validate step_user"""

        host_name = user_input[CONF_HOST_NAME]
        host_port = int(user_input[CONF_HOST_PORT])
        client = AsyncModbusTcpClient(host_name, host_port)
        await client.connect()
        if client.connected:
            await client.close()
            return None
        await client.close()
        return ("base", "failed_to_connect")
