"""General helpers"""

# pylint: disable=relative-beyond-top-level
import logging
from typing import Any
from homeassistant.config_entries import ConfigEntry
from ..const import CONF_DEVICE_MODEL

_LOGGER = logging.getLogger(__name__)


def get_parameter(config_entry: ConfigEntry, parameter: str, default_val: Any = None):
    """Get parameter from OptionsFlow or ConfigFlow"""
    if parameter in config_entry.options.keys():
        return config_entry.options.get(parameter)
    if parameter in config_entry.data.keys():
        return config_entry.data.get(parameter)
    return default_val


def get_device_model(config_entry: ConfigEntry):
    """Get device model selected during the integration setup or the options configuration"""
    if CONF_DEVICE_MODEL in config_entry.options:
        return config_entry.options[CONF_DEVICE_MODEL]
    else:
        return config_entry.data[CONF_DEVICE_MODEL]
