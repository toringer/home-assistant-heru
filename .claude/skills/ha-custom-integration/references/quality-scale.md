# Integration Quality Scale: checklist for custom integrations

Source: https://contributors.home-assistant.io/core/quality-scale/rules/. Each rule has its own page at `/core/quality-scale/rules/<rule-id>/index.md`. Fetch it when you need the exact requirement or exemptions.

Custom integrations aren't formally graded, but the rules are the shared definition of "good". Some rules assume core (the docs site, the brands repo). Their custom-integration equivalent is noted. To track status, a `quality_scale.yaml` in the integration folder (`rule-id: done | todo | exempt` + comment) is a fine convention.

**Output format for reviews**: one row per rule: `rule | status (done / partial / missing / exempt) | evidence (file:line) | fix`. Then a short prioritized list of the fixes that matter most for users.

## Bronze

| Rule | Verify in a custom integration |
|---|---|
| action-setup | Actions registered in `async_setup`, not `async_setup_entry`. Exempt if there are no actions. |
| appropriate-polling | `update_interval` sensible for the data (local device: 10–60 s typical). Not user-configurable. |
| brands | Custom integrations: `custom_components/<domain>/brand/icon.png` (+ `logo.png`, `@2x`, dark variants). Not the brands repo. |
| common-modules | Coordinator in `coordinator.py`, base entity in `entity.py`. |
| config-flow | `config_flow: true` in manifest + `config_flow.py`. Every field has `data_description`. Uses `data` for connection info, `options` for behaviour. |
| config-flow-test-coverage | `tests/test_config_flow.py` covers success, each error → recovery, duplicate abort, and reconfigure/reauth/options if present. |
| dependency-transparency | Requirements are PyPI packages with public source. Pinned or lower-bounded in manifest. |
| docs-actions / docs-conditions / docs-triggers / docs-high-level-description / docs-installation-instructions / docs-removal-instructions | Custom: README (or the `documentation` URL) covers these. |
| entity-event-setup | Subscriptions in `async_added_to_hass`, removed via `self.async_on_remove(...)`. |
| entity-unique-id | Every entity has a stable `unique_id`. **Fail it if the ID uses IP/host/user-editable values**: changing the IP then duplicates every entity. |
| has-entity-name | `_attr_has_entity_name = True` on all entities. Names are relative to the device ("Supply temperature", not "HERU supply temperature"). |
| runtime-data | `entry.runtime_data`, no `hass.data[DOMAIN]` for per-entry objects. Typed `ConfigEntry[...]` alias. |
| test-before-configure | Flow connects to the device before `async_create_entry`, maps failure to `cannot_connect`. |
| test-before-setup | `async_setup_entry` raises `ConfigEntryNotReady` / `AuthFailed` / `Error` when the device fails. `async_config_entry_first_refresh` counts. |
| unique-config-entry | `async_set_unique_id` + `_abort_if_unique_id_configured`, or `single_config_entry: true` in manifest. Prefer device serial/MAC over host. |

## Silver

| Rule | Verify |
|---|---|
| action-exceptions | Actions and entity commands raise `ServiceValidationError` (user error) / `HomeAssistantError` (device error), not raw library exceptions or `ValueError`. |
| config-entry-unloading | `async_unload_entry` unloads platforms and closes connections (`entry.async_on_unload`). Reload works without restart, with no stale globals. |
| docs-configuration-parameters / docs-installation-parameters | README documents each setup and option field. |
| entity-unavailable | `UpdateFailed` from the coordinator → entities unavailable. Push entities set `_attr_available`. |
| integration-owner | `codeowners` in manifest. |
| log-when-unavailable | Coordinator does this. Push: log once on loss and once on recovery. Don't log every poll. |
| parallel-updates | `PARALLEL_UPDATES` constant in **each** platform module. |
| reauthentication-flow | Exempt if there are no credentials (e.g. plain Modbus TCP). |
| test-coverage | >95 % per module (`pytest --cov=custom_components.<domain> --cov-report=term-missing`). |

## Gold

| Rule | Verify |
|---|---|
| devices | `DeviceInfo` with identifiers, name, manufacturer, model, sw_version/hw_version where known. `model` = hardware model, not integration version. |
| diagnostics | `diagnostics.py` with `async_redact_data` for host/credentials/serials. |
| discovery / discovery-update-info | zeroconf/dhcp/ssdp/usb matcher in manifest, plus a discovery step that updates host via `_abort_if_unique_id_configured(updates=...)`. Often exempt for devices that can't be discovered (state why). |
| docs-data-update / docs-examples / docs-known-limitations / docs-supported-devices / docs-supported-functions / docs-troubleshooting / docs-use-cases | README sections. |
| dynamic-devices | New sub-devices appear without reload (coordinator listener adds entities). Exempt for single-device integrations. |
| entity-category | Config entities `EntityCategory.CONFIG`, diagnostic ones `EntityCategory.DIAGNOSTIC`. |
| entity-device-class | Device class set wherever one exists (temperature, humidity, power, duration, timestamp, problem, …). |
| entity-disabled-by-default | Noisy / rarely used entities `entity_registry_enabled_default=False`. |
| entity-translations | `translation_key` + `entity` section in en.json. No hard-coded English `_attr_name` (except proper nouns/model names). |
| exception-translations | Exceptions raised to users use `translation_domain`/`translation_key`, with text under `exceptions` in en.json. |
| icon-translations | `icons.json` instead of `_attr_icon` / `icon` property (unless the icon is truly dynamic). |
| reconfiguration-flow | `async_step_reconfigure` for host/port etc. |
| repair-issues | `ir.async_create_issue` for user-fixable problems (e.g. wrong firmware). Exempt if there are none. |
| stale-devices | Remove devices that disappeared, or implement `async_remove_config_entry_device`. Exempt for a single fixed device. |

## Platinum

| Rule | Verify |
|---|---|
| async-dependency | The library is asyncio-native (pymodbus `AsyncModbusTcpClient` qualifies). |
| inject-websession | Pass `async_get_clientsession(hass)` to HTTP libraries. Exempt for non-HTTP (Modbus, serial). |
| strict-typing | `py.typed` dependency, full annotations, `mypy --strict` passes on the package. |
