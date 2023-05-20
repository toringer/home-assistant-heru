"""Adds config flow for HERU."""
import logging
from typing import Any, Optional
from custom_components.heru.helpers.config_flow import FlowValidator
from custom_components.heru.helpers.general import get_parameter
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_HOST_NAME,
    CONF_HOST_PORT,
    CONF_DEVICE_NAME,
    CONF_DEVICE_MODEL,
    DOMAIN,
    DEVICE_MODELS,
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
        return OptionsFlowHandler(config_entry)

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
            vol.Required(
                CONF_DEVICE_MODEL, default=DEVICE_MODELS[0]["value"]
            ): selector(
                {
                    "select": {
                        "options": DEVICE_MODELS,
                        "mode": "dropdown",
                    }
                }
            ),
            vol.Required(CONF_HOST_NAME): cv.string,
            vol.Required(CONF_HOST_PORT, default=502): cv.port,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(user_schema),
            errors=self._errors,
            last_step=True,
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler"""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._errors = {}

    async def async_step_init(self, user_input) -> FlowResult:
        """Manage the options."""

        self._errors = {}
        if user_input is not None:
            # process user_input
            error = await FlowValidator.validate_step_user(self.hass, user_input)
            if error is not None:
                self._errors[error[0]] = error[1]

            if not self._errors:
                return self.async_create_entry(
                    title=self.config_entry.title, data=user_input
                )

        user_schema = {
            vol.Required(
                CONF_HOST_NAME, default=get_parameter(self.config_entry, CONF_HOST_NAME)
            ): cv.string,
            vol.Required(
                CONF_DEVICE_MODEL,
                default=get_parameter(self.config_entry, CONF_DEVICE_MODEL),
            ): selector(
                {
                    "select": {
                        "options": DEVICE_MODELS,
                        "mode": "dropdown",
                    }
                }
            ),
            vol.Required(
                CONF_HOST_PORT, default=get_parameter(self.config_entry, CONF_HOST_PORT)
            ): cv.port,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(user_schema),
            errors=self._errors,
            last_step=True,
        )
