"""Helpers for config_flow"""

import logging
from typing import Any
from homeassistant.core import HomeAssistant


# pylint: disable=relative-beyond-top-level
from ..const import (
    CONF_HOST_PORT,
    CONF_HOST_NAME,
    DOMAIN,
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

        coordinator = None
        if DOMAIN in hass.data and "coordinator" in hass.data[DOMAIN]:
            coordinator = hass.data[DOMAIN]["coordinator"]
            if coordinator is not None:
                coordinator.pause()

        host_name = user_input[CONF_HOST_NAME]
        host_port = int(user_input[CONF_HOST_PORT])
        client = AsyncModbusTcpClient(host_name, port=host_port)
        await client.connect()
        if client.connected:
            client.close()
            return None
        client.close()

        if coordinator is not None:
            await coordinator.resume()
        return ("base", "failed_to_connect")
