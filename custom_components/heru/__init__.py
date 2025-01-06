"""HERU integration"""
import logging
import asyncio
from custom_components.heru.helpers.general import get_parameter
from custom_components.heru.heru_coordinator import HeruCoordinator

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core_config import Config  # Updated import

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
    client = AsyncModbusTcpClient(host=host_name, port=host_port)  # Updated instantiation

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = HeruCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN]["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

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
        coordinator = hass.data[DOMAIN]["coordinator"]
        if coordinator is not None:
            coordinator.close()
            hass.data[DOMAIN]["coordinator"] = None
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    _LOGGER.debug("async_reload_entry")
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
