"""Pytest fixtures for Fellow Stagg integration tests (Bronze/Gold: test coverage).

Requires pytest-homeassistant-custom-component for the hass fixture.
Run: pip install -r requirements_test.txt && pytest tests/
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.fellow_stagg.const import DOMAIN


# Enable custom integrations so custom_components.fellow_stagg is loadable (required for HA >= 2021.6)
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations (from pytest-homeassistant-custom-component)."""
    pass


@pytest.fixture(name="mock_validate_kettle")
def fixture_mock_validate_kettle() -> AsyncMock:
    """Mock validate_kettle_cli to avoid real HTTP calls."""
    with patch(
        "custom_components.fellow_stagg.config_flow.validate_kettle_cli",
        new_callable=AsyncMock,
        return_value=True,
    ) as mock:
        yield mock
