"""Adds config flow for HERU."""
import logging
from typing import Any, Optional
from custom_components.heru.helpers.config_flow import FlowValidator
from custom_components.heru.helpers.general import get_parameter, unique_id_prefix
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_HOST_NAME,
    CONF_HOST_PORT,
    CONF_DEVICE_NAME,
    CONF_FAN_CONTROL,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)


_LOGGER = logging.getLogger(__name__)


class HeruIqcConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    VERSION = 1
    user_input: Optional[dict[str, Any]]

    def __init__(self):
        """Initialize."""
        _LOGGER.debug("HeruIqcConfigFlow.__init__")
        self._errors = {}
        self.user_input = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("HeruIqcConfigFlow.async_step_user")
        self._errors = {}

        if user_input is None:
            user_input = {}
        else:
            # process user_input
            error = await FlowValidator.validate_step_user(self.hass, user_input)
            if error is not None:
                self._errors[error[0]] = error[1]

            if not self._errors:
                self.user_input = user_input
                return self.async_create_entry(
                    title=user_input[CONF_DEVICE_NAME], data=self.user_input
                )

        return await self._show_config_form_user(user_input)

    async def _show_config_form_user(self, user_input):
        """Show the configuration form."""

        user_schema = {
            vol.Required(CONF_DEVICE_NAME): cv.string,
            vol.Required(CONF_HOST_NAME): cv.string,
            vol.Required(CONF_HOST_PORT, default=502): cv.positive_int,
            vol.Required(CONF_FAN_CONTROL, default=False): cv.boolean
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(user_schema),
            errors=self._errors,
            last_step=True,
        )


@callback
def async_migrate_unique_ids(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    old_host_name: str,
    new_host_name: str,
) -> None:
    """Move the entities of a config entry to the unique ids of a new host.

    The unique ids contain the host, so without this a host change would
    register every entity a second time and orphan the existing ones.
    """
    old_prefix = f"{unique_id_prefix(old_host_name)}_"
    new_prefix = f"{unique_id_prefix(new_host_name)}_"
    if old_prefix == new_prefix:
        return

    registry = er.async_get(hass)
    for entity in er.async_entries_for_config_entry(registry, config_entry.entry_id):
        if not entity.unique_id.startswith(old_prefix):
            continue
        new_unique_id = new_prefix + entity.unique_id[len(old_prefix) :]
        if registry.async_get_entity_id(entity.domain, entity.platform, new_unique_id):
            _LOGGER.warning(
                "Not migrating %s, unique id %s is already in use",
                entity.entity_id,
                new_unique_id,
            )
            continue
        registry.async_update_entity(entity.entity_id, new_unique_id=new_unique_id)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler"""

    async def async_step_init(self, user_input) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # process user_input
            error = await FlowValidator.validate_step_user(self.hass, user_input)
            if error is not None:
                errors[error[0]] = error[1]

            if not errors:
                async_migrate_unique_ids(
                    self.hass,
                    self.config_entry,
                    get_parameter(self.config_entry, CONF_HOST_NAME),
                    user_input[CONF_HOST_NAME],
                )
                return self.async_create_entry(
                    title=self.config_entry.title, data=user_input
                )

        user_schema = {
            vol.Required(
                CONF_HOST_NAME, default=get_parameter(self.config_entry, CONF_HOST_NAME)
            ): cv.string,
            vol.Required(
                CONF_HOST_PORT, default=get_parameter(self.config_entry, CONF_HOST_PORT)
            ): cv.positive_int,
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=get_parameter(
                    self.config_entry, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
            ): vol.All(
                vol.Coerce(int),
                vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
            ),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(user_schema),
            errors=errors,
            last_step=True,
        )
