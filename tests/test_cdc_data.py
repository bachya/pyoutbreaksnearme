"""Define tests for interacting with user data."""

from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyoutbreaksnearme import Client
from tests.common import TEST_LATITUDE, TEST_LONGITUDE


@pytest.mark.asyncio
async def test_get_nearest_by_coordinate(
    aresponses: ResponsesMockServer, nonuserstats_us_response: dict[str, Any]
) -> None:
    """Test getting the nearest user data report to a latitude/longitude.

    Args:
        aresponses: An aresponses server.
        nonuserstats_us_response: An API response payload.
    """
    aresponses.add(
        "outbreaksnearme.org",
        "/api/nonuserstats/US",
        "get",
        response=aiohttp.web_response.json_response(
            nonuserstats_us_response, status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        nearest_user_data = await client.cdc_data.async_get_nearest_by_coordinates(
            TEST_LATITUDE, TEST_LONGITUDE
        )
        assert nearest_user_data == {
            "country": "US",
            "state": "New Mexico",
            "county": "Cibola",
            "confirmed": 8200,
            "death": 201,
            "iRateConfirm": 11115.2764761012,
            "iRateDeath": 272.45982581662696,
            "paintConfirm": "#474747",
            "paintDeath": "#474747",
        }

    aresponses.assert_plan_strictly_followed()
