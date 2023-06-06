"""HERU integration"""
import logging
import asyncio
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

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    _LOGGER.debug("async_unload_entry")

    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        client = hass.data[DOMAIN]["client"]
        if client is not None:
            await client.close()
            hass.data[DOMAIN]["client"] = None
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    _LOGGER.debug("async_reload_entry")
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
