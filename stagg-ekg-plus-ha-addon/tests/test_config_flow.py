"""Tests for Fellow Stagg config flow (Bronze: config-flow-test-coverage, Gold: test-coverage)."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.fellow_stagg.const import DOMAIN


@pytest.mark.asyncio
async def test_user_flow_manual_url(
    hass: HomeAssistant, mock_validate_kettle: AsyncMock
) -> None:
    """Test manual setup with base URL: user enters URL and integration is created."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"base_url": "http://192.168.1.32", "discover": False},
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {"base_url": "http://192.168.1.32"}
    assert result["title"] == "Fellow Stagg (http://192.168.1.32)"
    mock_validate_kettle.assert_called_once_with(hass, "http://192.168.1.32")


@pytest.mark.asyncio
async def test_user_flow_manual_url_normalized(
    hass: HomeAssistant, mock_validate_kettle: AsyncMock
) -> None:
    """Test that URL without scheme gets http:// prefix."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"base_url": "192.168.1.32", "discover": False},
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {"base_url": "http://192.168.1.32"}
    mock_validate_kettle.assert_called_once_with(hass, "http://192.168.1.32")


@pytest.mark.asyncio
async def test_user_flow_validation_fails(
    hass: HomeAssistant, mock_validate_kettle: AsyncMock
) -> None:
    """Test that form shows error when kettle validation fails."""
    mock_validate_kettle.return_value = False

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"base_url": "http://192.168.1.99", "discover": False},
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
async def test_user_flow_duplicate_unique_id(
    hass: HomeAssistant, mock_validate_kettle: AsyncMock
) -> None:
    """Test that duplicate base_url is rejected (unique_config_entry)."""
    # Add first entry via flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"base_url": "http://192.168.1.32", "discover": False},
    )
    # Try to add same URL again
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"base_url": "http://192.168.1.32", "discover": False},
    )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"
