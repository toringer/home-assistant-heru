# Where to look things up

Base: `https://contributors.home-assistant.io`. Add `index.md` to any page URL for clean Markdown (best for `curl -sL`). Old `developers.home-assistant.io/docs/...` links 301-redirect here.

Indexes for agents:
- `/llms.txt` lists the whole site. `/core/llms.txt` lists all ~190 core/integration pages with one-line descriptions. **Grep this first** when you don't know which page covers a topic.
- `/core/llms-full.txt` is the full text of every core page (~1.2 MB). Download it once and grep it (`grep -n "^Source: "` lists page boundaries). Don't load it whole into context.

## Most-used pages (`/core/...`, append `index.md`)

Integration building blocks, under `integrations/`:
- `file-structure/`, `manifest/`, `translations/`, `brands/`
- `config-entries/` (lifecycle, runtime_data, migration), `setup-failures/` (which exception when)
- `config-flow/`, `flow-steps/` (forms, menus, progress, selectors), `options-flow/`, `reauth-reconfigure/`, `subentries/`
- `fetching-data/` (coordinator), `events/`
- `device-registry/`, `entity-registry/` (unique-id migration)
- `actions/`, `diagnostics/`, `repairs/`, `discovery/`, `network-discovery/`

Entities, under `entities/`:
- Basics: `entity-class/`, `naming/`, `state-updates/`, `lifecycle/`, `state-attributes/`, `icons/`, `registry/`
- Platforms: `sensor/`, `binary-sensor/`, `climate/`, `fan/`, `number/`, `select/`, `switch/`, `button/`, `cover/`, `light/`, `water-heater/`, `update/`, … (the slug is the platform name with `-` for `_`)

Quality: `quality-scale/`, `quality-scale/rules/`, `quality-scale/rules/<rule-id>/`

Testing: `development/tests/` (core-oriented; see testing.md for custom-integration specifics)

Marketplace (custom integration publishing), under `/marketplace/`:
- `guides/integrations/` (layout, manifest keys required for custom, brand folder, validation)
- `reference/hacs-json/`, `reference/repository-structure/`, `reference/validation/`, `guides/releases/`

News: `/blog/` (deprecations, newest first). Each post states the version and removal date.

The official core skill (good context, written for core): https://raw.githubusercontent.com/home-assistant/core/dev/.claude/skills/ha-integration-knowledge/SKILL.md
