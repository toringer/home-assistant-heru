"""Helpers for config_flow"""

import logging
from typing import Any
from homeassistant.core import HomeAssistant


# pylint: disable=relative-beyond-top-level
from ..const import (
    CONF_HOST_PORT,
    CONF_HOST_NAME,
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
