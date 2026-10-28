# Current integration patterns (copy-ready)

Templates follow contributors.home-assistant.io as of HA 2026.10/11. Lines marked `# >=2026.11` need that minimum version; the comment next to them gives the fallback. Replace `example` / `Example` with the domain and class prefix.

## Contents
1. coordinator.py
2. __init__.py
3. entity.py
4. Platform with EntityDescription (sensor.py)
5. Command platform (switch/number/fan)
6. config_flow.py: user + reconfigure + options
7. translations/en.json
8. icons.json
9. diagnostics.py
10. Migrating unique IDs / config entry versions
11. Actions (services)

---

## 1. coordinator.py

```python
"""Coordinator for Example."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type ExampleConfigEntry = ConfigEntry[ExampleCoordinator]


@dataclass
class ExampleData:
    """Snapshot of the device state."""
    temperature: float | None
    fan_on: bool


class ExampleCoordinator(DataUpdateCoordinator[ExampleData]):
    """Fetch data for all Example entities."""

    config_entry: ExampleConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ExampleConfigEntry, client: ExampleClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
            always_update=False,  # only if ExampleData supports == (dataclasses do)
        )
        self.client = client

    async def _async_setup(self) -> None:
        """Runs once during first refresh; good for static device info."""
        self.device_info_raw = await self.client.get_device_info()

    async def _async_update_data(self) -> ExampleData:
        try:
            async with asyncio.timeout(10):
                raw = await self.client.read_all()
        except ExampleConnectionError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
                translation_placeholders={"error": str(err)},
            ) from err
        return ExampleData(temperature=raw.temp, fan_on=raw.fan)
```

The coordinator holds no mutable class-level dicts. Class attributes (`_regs = {}` at class level) are shared by *every* instance, so two config entries overwrite each other.

## 2. __init__.py

```python
"""The Example integration."""
from __future__ import annotations

from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import ExampleConfigEntry, ExampleCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:  # -> None on >=2026.11
    """Set up Example from a config entry."""
    client = ExampleClient(entry.data[CONF_HOST], entry.data[CONF_PORT])
    try:
        await client.connect()
    except ExampleConnectionError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
            translation_placeholders={"host": entry.data[CONF_HOST]},
        ) from err
    entry.async_on_unload(client.close)  # runs on every unload, including failed setups after this point

    coordinator = ExampleCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()  # raises ConfigEntryNotReady on failure
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True  # drop on >=2026.11


async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    # >=2026.11: await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS); return None
```

Not needed: `async_setup` returning True (only define it to register actions), `async_reload_entry`, `hass.data` bookkeeping. With `OptionsFlowWithReload` there is no update listener either.

If options must be applied *without* a reload, use a plain `OptionsFlow` plus:
```python
entry.async_on_unload(entry.add_update_listener(_async_update_listener))

async def _async_update_listener(hass: HomeAssistant, entry: ExampleConfigEntry) -> None:
    hass.config_entries.async_schedule_reload(entry.entry_id)  # or apply options in place
```
Never both a listener and a reloading flow helper.

## 3. entity.py

```python
"""Base entity for Example."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import ExampleCoordinator


class ExampleEntity(CoordinatorEntity[ExampleCoordinator]):
    """Common base for Example entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ExampleCoordinator, key: str) -> None:
        super().__init__(coordinator)
        device_id = coordinator.config_entry.unique_id or coordinator.config_entry.entry_id
        self._attr_unique_id = f"{device_id}_{key}"
        self._attr_device_info = DeviceInfo(  # keyword args: valid for TypedDict (<2026.11) and dataclass (>=2026.11)
            identifiers={(DOMAIN, device_id)},
            name=coordinator.config_entry.title,
            manufacturer=MANUFACTURER,
            model=coordinator.device_info_raw.model,
            sw_version=coordinator.device_info_raw.firmware,
        )
```

`model` is the hardware model, not the integration version. Use `sw_version` for firmware.

## 4. Platform with EntityDescription (sensor.py)

```python
"""Sensors for Example."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ExampleConfigEntry, ExampleCoordinator, ExampleData
from .entity import ExampleEntity

PARALLEL_UPDATES = 0  # read-only, coordinator does the I/O


@dataclass(frozen=True, kw_only=True)
class ExampleSensorEntityDescription(SensorEntityDescription):
    value_fn: Callable[[ExampleData], float | str | None]


SENSORS: tuple[ExampleSensorEntityDescription, ...] = (
    ExampleSensorEntityDescription(
        key="supply_temperature",
        translation_key="supply_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda d: d.supply_temp,
    ),
    ExampleSensorEntityDescription(
        key="filter_days",
        translation_key="filter_days",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda d: d.filter_days,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ExampleConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    async_add_entities(ExampleSensor(coordinator, d) for d in SENSORS)


class ExampleSensor(ExampleEntity, SensorEntity):
    entity_description: ExampleSensorEntityDescription

    def __init__(self, coordinator: ExampleCoordinator, description: ExampleSensorEntityDescription) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> float | str | None:
        return self.entity_description.value_fn(self.coordinator.data)
```

`AddConfigEntryEntitiesCallback` was added in 2025.2. On older minimums, use `AddEntitiesCallback`.

## 5. Command platform

```python
PARALLEL_UPDATES = 1  # serialize writes to the device

class ExampleSwitch(ExampleEntity, SwitchEntity):
    async def async_turn_on(self, **kwargs: Any) -> None:
        try:
            await self.coordinator.client.write_coil(self.entity_description.address, True)
        except ExampleConnectionError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="write_failed",
                translation_placeholders={"error": str(err)},
            ) from err
        await self.coordinator.async_request_refresh()
```

## 6. config_flow.py

```python
"""Config flow for Example."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol  # aliased to probatio on >=2026.9; keep what the file already uses

from homeassistant.config_entries import (
    ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlowWithReload,
)
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import CONF_FAN_CONTROL, DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {vol.Required(CONF_HOST): str, vol.Required(CONF_PORT, default=DEFAULT_PORT): int}
)
OPTIONS_SCHEMA = vol.Schema({vol.Required(CONF_FAN_CONTROL, default=False): bool})


async def _validate(hass, data: dict[str, Any]) -> str:
    """Connect and return a stable device identifier (serial/MAC). Raises CannotConnect."""
    ...


class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                serial = await _validate(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(serial)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"Example {serial}", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(STEP_USER_SCHEMA, user_input),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            try:
                serial = await _validate(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(serial)
                self._abort_if_unique_id_mismatch()  # needs "unique_id_mismatch" abort string
                return self.async_update_reload_and_abort(entry, data_updates=user_input)
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(STEP_USER_SCHEMA, entry.data),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> ExampleOptionsFlow:
        return ExampleOptionsFlow()


class ExampleOptionsFlow(OptionsFlowWithReload):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(OPTIONS_SCHEMA, self.config_entry.options),
        )
```

If existing entries have **no** `unique_id` (created by an older flow), `_abort_if_unique_id_mismatch` aborts every reconfigure. Either set the unique id on old entries in `async_migrate_entry` / during setup (`hass.config_entries.async_update_entry(entry, unique_id=...)`), or skip the mismatch check when `entry.unique_id is None`.

Reauth (only when there are credentials): `async_step_reauth(entry_data)` → `async_step_reauth_confirm` → `self.async_update_reload_and_abort(self._get_reauth_entry(), data_updates=...)`.

## 7. translations/en.json

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Connect to Example",
        "data": { "host": "Host", "port": "Port" },
        "data_description": {
          "host": "Hostname or IP address of the Example unit.",
          "port": "Modbus TCP port, usually 502."
        }
      },
      "reconfigure": {
        "title": "Change connection",
        "data": { "host": "Host", "port": "Port" },
        "data_description": {
          "host": "Hostname or IP address of the Example unit.",
          "port": "Modbus TCP port, usually 502."
        }
      }
    },
    "error": {
      "cannot_connect": "Failed to connect",
      "unknown": "Unexpected error"
    },
    "abort": {
      "already_configured": "Device is already configured",
      "reconfigure_successful": "Re-configuration was successful",
      "unique_id_mismatch": "The new address points to a different device."
    }
  },
  "options": {
    "step": {
      "init": {
        "data": { "fan_control": "Enable fan control" },
        "data_description": { "fan_control": "Expose a fan entity to control airflow." }
      }
    }
  },
  "entity": {
    "sensor": {
      "supply_temperature": { "name": "Supply air temperature" },
      "operating_mode": {
        "name": "Operating mode",
        "state": { "normal": "Normal", "boost": "Boost" }
      }
    }
  },
  "exceptions": {
    "cannot_connect": { "message": "Could not connect to {host}." },
    "update_failed": { "message": "Error communicating with device: {error}" },
    "write_failed": { "message": "Writing to the device failed: {error}" }
  }
}
```

The core docs say `reconfigure_successful` / `reauth_successful` come from HA. That's true for core via `strings.json` common keys, but in custom integrations `[%key%]` references don't resolve, so include the text yourself.

## 8. icons.json (next to manifest.json)

```json
{
  "entity": {
    "sensor": {
      "filter_days": { "default": "mdi:air-filter" },
      "operating_mode": {
        "default": "mdi:fan",
        "state": { "boost": "mdi:fan-plus" }
      }
    }
  }
}
```

## 9. diagnostics.py (Gold)

```python
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_HOST, CONF_PASSWORD

TO_REDACT = {CONF_HOST, CONF_PASSWORD}

async def async_get_config_entry_diagnostics(hass, entry: ExampleConfigEntry) -> dict[str, Any]:
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "options": dict(entry.options),
        "data": dataclasses.asdict(entry.runtime_data.data),
    }
```

## 10. Migrations

Config entry version bump (e.g. adding unique_id or changing data shape):
```python
async def async_migrate_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    if entry.version > 1:
        return False  # downgrade not supported (>=2026.11: raise ConfigEntryError)
    if entry.version == 1 and entry.minor_version < 2:
        hass.config_entries.async_update_entry(entry, data={...}, minor_version=2)
    return True
```

Entity unique_id scheme change (keeps history and customizations):
```python
from homeassistant.helpers import entity_registry as er

@callback
def _migrate(entity_entry: er.RegistryEntry) -> dict[str, Any] | None:
    if entity_entry.unique_id.startswith(old_prefix):
        return {"new_unique_id": entity_entry.unique_id.replace(old_prefix, new_prefix, 1)}
    return None

await er.async_migrate_entries(hass, entry.entry_id, _migrate)
```
Call this in `async_setup_entry` before forwarding platforms, or in `async_migrate_entry` with a version bump.

## 11. Actions

Register once in `async_setup(hass, config)`. Look up the entry from `call.data["config_entry_id"]` and check that `entry.state is ConfigEntryState.LOADED`, else raise `ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")`. Describe the action in `services.yaml`, with names under `services` in en.json.
