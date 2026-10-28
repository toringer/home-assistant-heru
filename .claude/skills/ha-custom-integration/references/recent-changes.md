# API changes that affect custom integrations (2024 – late 2026)

Compiled from https://contributors.home-assistant.io/blog/ (index of all posts; filter "Core and integrations"). Before relying on an exact version, re-read the linked post. For anything after this list, skim the blog index.

How to use it: compare each row's "since" version with the integration's **minimum** HA version (`hacs.json`). If `since` > minimum, the new form may not exist for some users. Keep the old form, or propose bumping the minimum.

| Since | Change | Old → New | Old form dies | Post |
|---|---|---|---|---|
| 2024.x | `runtime_data` on ConfigEntry | `hass.data[DOMAIN][...]` → `entry.runtime_data` + `type XConfigEntry = ConfigEntry[...]` | still works, Bronze rule | /core/integrations/config-entries/ |
| 2024.11 | OptionsFlow gets `self.config_entry` automatically | `OptionsFlowHandler(config_entry)` storing `self.config_entry = ...` → `OptionsFlowHandler()` | setting it explicitly errors from 2025.12 | — |
| 2024.x | Reconfigure helpers | custom update+reload → `_get_reconfigure_entry()`, `async_update_reload_and_abort(entry, data_updates=...)`, `_abort_if_unique_id_mismatch()` | — | /core/integrations/reauth-reconfigure/ |
| 2025.2 | `AddConfigEntryEntitiesCallback` type | `AddEntitiesCallback` in config-entry platforms → `AddConfigEntryEntitiesCallback` | typing only | — |
| 2025.8 (approx.) | `OptionsFlowWithReload` | update listener that reloads → subclass `OptionsFlowWithReload` | — | /core/integrations/options-flow/ |
| 2026.6 | Listener + reloading flow method deprecated | don't combine `add_update_listener` with `async_update_reload_and_abort` / `OptionsFlowWithReload` / `_abort_if_unique_id_configured` (reload) → use one; or `async_update_and_abort`, or `reload_on_update=False` | **error from 2026.12** | /blog/2026/05/07/config-entry-listener-together-with-reloading-methods/ |
| 2026.5 | Advanced mode in data entry flows deprecated | `self.show_advanced_options` → don't gate fields on it | — | /blog/2026/05/26/advanced-mode-config-flow-deprecation/ |
| 2026.4 | Entity IDs with mismatched domain deprecated | setting `entity_id = "sensor.x"` on a non-sensor → don't set entity_id manually | — | /blog/2026/04/07/entity-id-mismatched-domain-deprecated/ |
| 2026.6 | New unit enumerators | string units → `UnitOf*` enums from `homeassistant.const` | — | /blog/2026/06/30/new-unit-enumerators/ |
| 2026.7 | Devices: one config entry, ≤1 subentry | sharing devices across entries → not allowed | enforced 2026.9 | /blog/2026/07/21/device-registry-single-config-entry/ |
| 2026.8 | More device registry deprecations | see post (`async_get_or_create` args, new helpers) | — | /blog/2026/08/24/device-registry-follow-up-changes/ |
| 2026.9 | Probatio replaces voluptuous | `import voluptuous as vol` keeps working (alias). Core uses `import probatio`. Error message texts changed (update tests asserting on them) | no removal announced | /blog/2026/09/30/probatio-validation-engine/ |
| 2026.9 | Migration may raise ConfigEntry exceptions | `return False` from `async_migrate_entry` → raise `ConfigEntryError` / `ConfigEntryNotReady` | — | /blog/2026/09/17/Use-config-entry-exc-in-migration/ |
| 2026.9 | OAuth2 error handling moved into helper | catch-and-convert in integration → let helper handle | — | /blog/2026/09/07/oauth2-central-error-handling/ |
| 2026.9 | `modbus.get_hub` deprecated | (only if depending on the core modbus integration) → `async_get_unit` | — | /blog/2026/09/02/modbus-get-hub-deprecation/ |
| 2026.10 | `RestoreStateData.last_states` removed | use `async_get_last_state()` on RestoreEntity | removed | /blog/2026/10/06/restore-state-last-states-removal/ |
| 2026.11 | **Setup/unload/migrate return `None`** | `return True/False` → return nothing, raise `ConfigEntry*` on failure. `async_unload_platforms_or_raise` added. Custom integrations returning bool still work. **On HA < 2026.11, returning None from `async_setup_entry` = failure**, so keep `return True` while the minimum is older | no removal for custom | /blog/2026/10/23/config-entry-methods-return-none/ |
| 2026.11 | **`step_id` required on flow results** | `async_show_form(data_schema=...)` → `async_show_form(step_id="user", ...)` (also menu/progress/external_step) | **required 2027.5** | /blog/2026/10/23/flow-results-require-step-id/ |
| 2026.11 | **`DeviceInfo` is a dataclass** | dict literal / `info["name"]` / `.get()` / `.update()` / `**device_info` → `DeviceInfo(name=...)`, `info.name`, `async_get_or_create_from_info`. Unset fields are `UNDEFINED` (truthy!). Deprecated fields `default_*`, `via_device` → `name`/`manufacturer`/`model`, `via_device_id` | `[]`/`.get()` compat layer: later. `via_device` 2027.8, `default_*` 2027.9 | /blog/2026/10/13/device-info-class/ |
| 2026.11 | **Climate native temperatures** | `current_temperature`, `target_temperature(_high/_low)`, `temperature_unit` (+ `_attr_`) → `native_*` equivalents. `min_temp`/`max_temp`/`target_temperature_step` unchanged | **2027.11** | /blog/2026/10/08/climate-native-temperature/ |
| 2026.11 | Water heater native temperatures | same as climate | 2027.11 | /blog/2026/10/08/water-heater-native-temperature/ |
| 2026.11 | Repair issues can belong to a config entry | see post | — | /blog/2026/10/28/issue-registry-refresh/ |

Prefix relative links with `https://contributors.home-assistant.io`.

## Long-standing rules that code from memory often gets wrong

- `async_timeout` package → `asyncio.timeout` (Python 3.11+).
- `async_add_devices` param name → `async_add_entities` (the name doesn't matter functionally, but match the docs).
- `hass.config_entries.async_forward_entry_setup` (singular) was removed in 2025.x → `async_forward_entry_setups(entry, PLATFORMS)`.
- Gathering `async_forward_entry_unload` per platform → `async_unload_platforms(entry, PLATFORMS)`.
- `FlowResult` from `data_entry_flow` → `ConfigFlowResult` from `config_entries`.
- `DataUpdateCoordinator` without `config_entry=` logs a warning for custom integrations and will break. Always pass it.
- `self.hass.helpers.*` and `hass.components.*` accessors were removed. Import the helpers.
- `entity.async_write_ha_state()` from a thread → `self.schedule_update_ha_state()` / `hass.add_job`. Everything in an integration should be async anyway.
