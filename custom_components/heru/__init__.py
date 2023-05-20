"""HERU integration"""
import logging
from custom_components.heru.helpers.general import get_parameter

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

from pymodbus.client import (
    AsyncModbusTcpClient,
)

from .const import (
    CONF_HOST_NAME,
    CONF_HOST_PORT,
    DOMAIN,
    PLATFORMS,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(
    hass: HomeAssistant, config: Config
):  # pylint: disable=unused-argument
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    _LOGGER.debug("async_setup_entry")
    host_name = get_parameter(entry, CONF_HOST_NAME)
    host_port = int(get_parameter(entry, CONF_HOST_PORT))
    client = AsyncModbusTcpClient(host_name, host_port)
    await client.connect()
    assert client.connected
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN]["client"] = client

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            _LOGGER.debug("async_forward_entry_setup")
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    _LOGGER.debug("async_unload_entry")
    client = hass.data[DOMAIN]["client"]
    await client.close()
    hass.data[DOMAIN]["client"] = None
    return True


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        new = {**config_entry.data}
        # TODO: modify Config Entry data

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True


# async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
#     """Reload config entry."""
# TODO
#     _LOGGER.debug("async_reload_entry")
#     await async_unload_entry(hass, entry)
#     await async_setup_entry(hass, entry)
