# Testing a custom integration

Core tests use `tests/common.py` from the core repo. Custom integrations get the same fixtures from **pytest-homeassistant-custom-component** (PyPI), which is released for every HA version. Pin it to the version whose HA matches `requirements_dev.txt` (check `pip index versions pytest-homeassistant-custom-component` and the package's changelog, or let pip resolve `pytest-homeassistant-custom-component` alongside the pinned `homeassistant`). It pins its own `homeassistant`, so don't pin both to conflicting versions.

## Layout

```
tests/
  __init__.py
  conftest.py
  test_config_flow.py
  test_init.py          # setup, unload, retry on failure
  test_sensor.py        # optional: snapshot_platform
pyproject.toml / setup.cfg: asyncio_mode = "auto", testpaths = ["tests"]
```

## conftest.py

```python
"""Fixtures for Example tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.example.const import DOMAIN

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Custom integrations are not loaded in tests unless enabled."""
    yield


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    # return_value=True on HA < 2026.11, None on >= 2026.11
    with patch("custom_components.example.async_setup_entry", return_value=True) as m:
        yield m


@pytest.fixture
def mock_client() -> Generator[MagicMock]:
    """Patch the library client where the integration imports it (every module that imports it)."""
    with (
        patch("custom_components.example.ExampleClient", autospec=True) as m,
        patch("custom_components.example.config_flow.ExampleClient", new=m),
    ):
        client = m.return_value
        client.connect.return_value = True
        client.read_all.return_value = ...
        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="Example",
        data={"host": "192.168.1.10", "port": 502},
        unique_id="SERIAL123",  # match what the flow sets; omit if entries have none
    )
```

## test_config_flow.py

```python
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_success(hass: HomeAssistant, mock_client, mock_setup_entry) -> None:
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"host": "1.2.3.4", "port": 502})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {"host": "1.2.3.4", "port": 502}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_user_flow_cannot_connect_then_recovers(hass, mock_client, mock_setup_entry) -> None:
    mock_client.connect.side_effect = ConnectionError
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"host": "1.2.3.4", "port": 502})
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    mock_client.connect.side_effect = None
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"host": "1.2.3.4", "port": 502})
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_duplicate_aborts(hass, mock_client, mock_config_entry) -> None:
    mock_config_entry.add_to_hass(hass)
    ...
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reconfigure(hass, mock_client, mock_setup_entry, mock_config_entry) -> None:
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reconfigure_flow(hass)
    assert result["step_id"] == "reconfigure"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"host": "5.6.7.8", "port": 502})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert mock_config_entry.data["host"] == "5.6.7.8"


async def test_options(hass, mock_client, mock_config_entry) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)
    result = await hass.config_entries.options.async_configure(result["flow_id"], {"fan_control": True})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert mock_config_entry.options == {"fan_control": True}
```

(`start_reconfigure_flow` exists on `MockConfigEntry` in recent versions. On old ones, call `flow.async_init(DOMAIN, context={"source": SOURCE_RECONFIGURE, "entry_id": entry.entry_id})`.)

## test_init.py

```python
from homeassistant.config_entries import ConfigEntryState

async def test_setup_and_unload(hass, mock_client, mock_config_entry) -> None:
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.example_supply_air_temperature") is not None

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_retry_when_offline(hass, mock_client, mock_config_entry) -> None:
    mock_client.read_all.side_effect = ConnectionError
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
```

## Gotchas

- `enable_custom_integrations` must be active, or HA says "Integration not found".
- Patch where the name is **used** (`custom_components.example.coordinator.Client`), not where it's defined (`library.Client`).
- Don't assert on coordinator internals or call entity methods directly. Go through `hass.states` / `hass.services.async_call(..., blocking=True)`.
- Time: use the `freezer` fixture + `async_fire_time_changed`, never patch `utcnow`.
- After Probatio (2026.9), voluptuous error message strings differ. Don't assert on schema error text.
- No network access in tests. pytest-socket blocks it, so unpatched clients fail loudly.
- Run: `python -m pytest tests -q` (add `--cov=custom_components.example --cov-report=term-missing`).
