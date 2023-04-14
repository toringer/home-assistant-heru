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


_LOGGER = logging.getLogger(__name__)


class FlowValidator:
    """Validator of flows"""

    @staticmethod
    def validate_step_user(
        hass: HomeAssistant, user_input: dict[str, Any]
    ) -> list[str]:
        """Validate step_user"""

        entity_registry: EntityRegistry = async_entity_registry_get(hass)
        entities = entity_registry.entities

        return None
