---
name: ha-custom-integration
description: Build, modernize, test, and review Home Assistant custom integrations (custom_components/<domain>, HACS/Marketplace) following the official contributor docs at contributors.home-assistant.io. Use this skill whenever the work touches a Home Assistant integration's Python or JSON files — __init__.py, coordinator, config_flow.py / options / reconfigure / reauth flows, entity platforms (sensor, climate, fan, number, switch, button, binary_sensor…), manifest.json, hacs.json, translations/en.json, icons.json, diagnostics, repairs, or pytest tests — and whenever the user mentions the integration quality scale, hassfest, HACS validation, deprecation warnings in the HA log, or upgrading to a new Home Assistant release, even if they don't say "skill" or "best practice".
---

# Home Assistant custom integrations

Home Assistant's integration API moves fast. Something changes almost every monthly release, and deprecations are announced on the contributors blog. Code written from memory tends to use patterns that are 1–3 years old (`hass.data[DOMAIN]`, dict `device_info`, hard-coded entity names, `voluptuous`, update listeners next to reloading flows). Your job is to write code that matches **current** docs while still running on the **oldest HA version the integration supports**.

Two sources of truth, in this order:

1. **The installed `homeassistant` package.** If an API isn't there, it doesn't exist for this project yet, whatever the docs say.
2. **The docs at contributors.home-assistant.io**, which replaced developers.home-assistant.io (old URLs 301-redirect there). Every page has a Markdown version: add `index.md` to the URL. [references/docs-map.md](references/docs-map.md) lists the pages you'll need most.

## Workflow

### 1. Establish the version window

Before writing code, find out:

- **Minimum HA version**: `hacs.json` → `"homeassistant"`. Users on this version must keep working.
- **Dev/test HA version**: `requirements_dev.txt` / `requirements*.txt`, or `python -c "from homeassistant.const import __version__; print(__version__)"`.
- **Current HA release**: newer than both, usually. Check https://pypi.org/pypi/homeassistant/json if it matters.

This window decides which API you may use. A custom integration can't simply adopt everything in the docs: many examples there show APIs added in the latest release. Rules:

- If the API exists in the minimum version, use the modern form.
- If it was added after the minimum version, either keep the older form that still works (most deprecations last 12 months for custom integrations), or propose bumping `hacs.json`'s minimum, and say so explicitly. Don't silently raise the minimum.
- When unsure whether something exists, check the installed package. That beats guessing:
  ```bash
  python -c "import homeassistant.config_entries as m; print(hasattr(m, 'OptionsFlowWithReload'))"
  grep -rn "def async_unload_platforms_or_raise" "$(python -c 'import homeassistant,os;print(os.path.dirname(homeassistant.__file__))')"
  ```
  For a version older than the installed one, check the git tag on GitHub (`https://raw.githubusercontent.com/home-assistant/core/<version>/homeassistant/...`).

[references/recent-changes.md](references/recent-changes.md) lists the 2024–2026 changes with the version each one landed in. Read it whenever you touch setup, flows, devices, climate entities, or schemas, and before any "modernize"/"upgrade"/"fix deprecation warnings" task.

### 2. Read the code and the relevant docs

Read the integration's existing files before editing. Match its naming, comment density and structure. A focused change shouldn't turn into a rewrite.

When you're about to use an API you haven't verified in this session (a flow helper, entity property, coordinator argument, exception type), fetch the doc page rather than relying on memory. Use `curl -sL <url>index.md`, or WebFetch with a specific question. It takes a few seconds and prevents most "that method doesn't exist / was renamed" bugs.

### 3. Implement with the current patterns

[references/patterns.md](references/patterns.md) has copy-ready templates for each file. The essentials, and why they matter:

**Setup and lifecycle**
- Store per-entry objects in `entry.runtime_data`, typed as `type XConfigEntry = ConfigEntry[XCoordinator]` (in `coordinator.py`). `hass.data[DOMAIN]` is shared across entries, so a second device overwrites the first, and it isn't cleaned up on unload. Set `runtime_data` *before* `async_forward_entry_setups`.
- Signal failure with exceptions, not return values: `ConfigEntryNotReady` (offline, retry), `ConfigEntryAuthFailed` (start reauth), `ConfigEntryError` (permanent). Raise them from the integration's `async_setup_entry`. Raised from a platform's `async_setup_entry`, they're only logged.
- Return values: since 2026.11, setup/unload/migrate return `None`. On older HA a non-bool return from `async_setup_entry` is treated as a failure, so if the minimum version is below 2026.11, keep `-> bool` and `return True`.
- Unload with `hass.config_entries.async_unload_platforms(entry, PLATFORMS)`. Register cleanup with `entry.async_on_unload(...)` so it runs on every unload path.
- Don't write your own reload function (unload + setup). Use `hass.config_entries.async_schedule_reload(entry.entry_id)` or `OptionsFlowWithReload`.

**Coordinator** (`coordinator.py`, a Bronze rule called *common-modules*)
- `DataUpdateCoordinator[DataType]`, pass `config_entry=`, and return the data from `_async_update_data`. Entities read `self.coordinator.data`. Keeping state in class attributes instead of returning it breaks `always_update=False`, diagnostics and tests.
- Raise `UpdateFailed` (translated, `from err`). The coordinator logs once, marks entities unavailable, and logs recovery. That covers the Silver rules *entity-unavailable* and *log-when-unavailable*.
- Use the `asyncio.timeout` builtin. `async_timeout` is deprecated.
- After a write command, call `await coordinator.async_request_refresh()` (debounced), not `async_refresh()`.
- Polling interval is fixed by the integration and isn't a user option.

**Entities**
- `_attr_has_entity_name = True` and `_attr_translation_key = "..."`, with names in `translations/en.json` under `entity.<platform>.<key>.name`. Set `_attr_name = None` for the device's main entity. Leave the name unset to get the device-class name.
- Icons go in `icons.json` (keyed by translation key), not `_attr_icon`. `icon` is written to the database on every state change.
- `unique_id` must be stable and never change: serial number or MAC, falling back to `entry.unique_id` or `entry.entry_id`. **Never use an IP address, host, or user-editable name.** If you change an existing unique_id scheme, migrate it in the entity registry (`er.async_migrate_entries` in `async_migrate_entry`), or users lose their entity history and customizations.
- `device_info`: construct with `DeviceInfo(identifiers={(DOMAIN, id)}, name=..., manufacturer=..., model=..., sw_version=...)` keyword arguments. That works both before and after 2026.11, when it became a dataclass. Don't build a dict literal, and don't use `info["key"]` or `.get()`.
- Use `EntityDescription` subclasses (`@dataclass(frozen=True, kw_only=True)`) with a `value_fn` for tables of similar entities, rather than dicts with string keys.
- Set `PARALLEL_UPDATES` in each platform module: `0` for coordinator-only read platforms, `1` for platforms that send commands to a device that can't handle concurrent writes.
- Use `entity_category`, `device_class`, `state_class` and `entity_registry_enabled_default=False` where they apply.
- When overriding `available`, return `super().available and ...`.
- Climate: from 2026.11, temperatures use `native_*` names (`native_current_temperature`, `native_temperature_unit`, …). Old names work until 2027.11. Check the version window.

**Config flow**
- `await self.async_set_unique_id(<stable id>)` + `self._abort_if_unique_id_configured()` in every creating step. Get the stable id from the device during validation; for a local device, only fall back to host when nothing better exists.
- Test the connection before `async_create_entry` (Bronze: *test-before-configure*). Map known errors to `cannot_connect`, `invalid_auth` etc. without logging. For unexpected exceptions, use `_LOGGER.exception` + `unknown`.
- Always pass `step_id=` to `async_show_form` / `async_show_menu` / `async_show_progress` / `async_external_step`. It's deprecated to omit it, and required from 2027.5.
- Reconfigure: `async_step_reconfigure` + `self._get_reconfigure_entry()` + `self._abort_if_unique_id_mismatch()` + `self.async_update_reload_and_abort(entry, data_updates=...)`.
- Options flow: `async_get_options_flow` returns `XOptionsFlow()` with **no arguments**. Use `self.config_entry` inside the steps, never in `__init__`. Prefer `OptionsFlowWithReload`.
- **Don't combine an update listener (`entry.add_update_listener`) with reloading flow helpers** (`OptionsFlowWithReload`, `async_update_reload_and_abort`, or `_abort_if_unique_id_configured` with reload). It reloads twice and races. Deprecated since 2026.6, and an error from 2026.12. Pick one mechanism.
- Every form field needs `data` and `data_description` in translations. Don't ask for a name or polling interval.
- `import voluptuous as vol` still works (aliased to Probatio since 2026.9). Keep whatever the file already uses, and don't churn imports.

**Translations for custom integrations**
- Ship `translations/en.json` (complete, it's the fallback) plus other languages. Custom integrations don't use `strings.json`, and `[%key:common::...%]` references **don't resolve** in custom integrations, so write the full text.
- Add new keys to **every** language file in `translations/`. At least copy the English text into the others and say so, so hassfest passes and nothing shows a raw key.

**Actions (services)**: register in `async_setup` (once per integration, not per entry), describe them in `services.yaml`, and raise `ServiceValidationError` / `HomeAssistantError` with translation keys.

### 4. Test

Custom integrations test with `pytest-homeassistant-custom-component` (pin it to the version matching the dev HA version). See [references/testing.md](references/testing.md) for conftest, the config-flow test template and gotchas. Principles:
- Test through Home Assistant (`hass.config_entries.async_setup`, `hass.states.get`, `hass.services.async_call`). Patch the **library client where the integration imports it**, never the coordinator or entity internals.
- Config flow: cover success, every error followed by recovery to success, and duplicate abort.
- Run the tests you wrote. If they can't run in this environment, say so rather than implying they pass.

### 5. Validate

- hassfest + HACS action (usually already in `.github/workflows`). Locally, at minimum, check that every `translation_key` used in code exists in `en.json`, the JSON parses, and the manifest has `version`, `issue_tracker`, `codeowners`, `documentation`, and `iot_class`.
- Run the repo's formatter or linter (black/ruff) if it has one configured.
- Check the HA log after a dev-instance start for deprecation warnings mentioning the domain.

## Reviewing against the quality scale

When asked to review or "check against best practices / the quality scale", use [references/quality-scale.md](references/quality-scale.md). It lists all rules by tier with how to verify each in a custom integration. Report per rule: **done / not done / exempt (why)**, with file:line evidence and the concrete fix. Bronze first. Rank findings by user impact: unique-id bugs and broken unload/reload hurt users, while missing docs pages don't.

## Scope boundaries

- Protocol logic (register maps, parsing, device state machines) belongs in a PyPI library. That's the docs' guidance for core. For an existing custom integration, mention it as a recommendation; don't restructure the project unprompted.
- Deprecation timelines in recent-changes.md were taken from the blog as of late 2026. When a task hinges on an exact version, re-check the blog post (linked in that file).
