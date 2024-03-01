"""Define tests for interacting with user data."""

import logging
from typing import Any
from unittest.mock import Mock

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyoutbreaksnearme import Client
from pyoutbreaksnearme.errors import RequestError
from tests.common import TEST_LATITUDE, TEST_LONGITUDE


@pytest.mark.asyncio
async def test_get_nearest_by_coordinate(
    aresponses: ResponsesMockServer, caplog: Mock, markers_us_response: dict[str, Any]
) -> None:
    """Test getting the nearest user data report to a latitude/longitude.

    Args:
        aresponses: An aresponses server.
        caplog: A mocked logging utility.
        markers_us_response: An API response payload.
    """
    caplog.set_level(logging.DEBUG)

    aresponses.add(
        "outbreaksnearme.org",
        "/api/markers/US",
        "get",
        response=aiohttp.web_response.json_response(markers_us_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
            TEST_LATITUDE, TEST_LONGITUDE
        )
        assert nearest_user_data == {
            "fluSymptoms": 0,
            "noSymptoms": 0,
            "otherSymptoms": 0,
            "symptoms": 1,
            "zipcode": "10002",
        }

    assert any(m for m in caplog.messages if "Data returned for /markers/US" in m)
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_nearest_by_coordinate_no_session(
    aresponses: ResponsesMockServer, markers_us_response: dict[str, Any]
) -> None:
    """Test getting the nearest user data report to a latitude/longitude.

    This test is here to test not explicitly providing a ClientSession.

    Args:
        aresponses: An aresponses server.
        markers_us_response: An API response payload.
    """
    aresponses.add(
        "outbreaksnearme.org",
        "/api/markers/US",
        "get",
        response=aiohttp.web_response.json_response(markers_us_response, status=200),
    )

    client = Client()
    nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
        TEST_LATITUDE, TEST_LONGITUDE
    )
    assert nearest_user_data == {
        "fluSymptoms": 0,
        "noSymptoms": 0,
        "otherSymptoms": 0,
        "symptoms": 1,
        "zipcode": "10002",
    }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_totals(
    aresponses: ResponsesMockServer,
    stats_us_response: dict[str, Any],
    usersubmission_stats_region_noa_response: dict[str, Any],
) -> None:
    """Test getting the nearest user data report to a latitude/longitude.

    Args:
        aresponses: An aresponses server.
        stats_us_response: An API response payload.
        usersubmission_stats_region_noa_response: An API response payload.
    """
    aresponses.add(
        "outbreaksnearme.org",
        "/api/usersubmission/stats/region/NOA",
        "get",
        response=aiohttp.web_response.json_response(
            usersubmission_stats_region_noa_response, status=200
        ),
    )
    aresponses.add(
        "outbreaksnearme.org",
        "/api/stats/US",
        "get",
        response=aiohttp.web_response.json_response(stats_us_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        user_data_totals = await client.user_data.async_get_totals()
        assert user_data_totals == {
            "usersubmissioncountforregion": 6993340,
            "covidsymptoms": 2370,
            "nosymptoms": 15314,
            "othersymptoms": 175,
            "flulikesymptoms": 535,
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_totals_error(aresponses: ResponsesMockServer) -> None:
    """Test an error while getting the nearest user data report.

    This is a sanity check to ensure we cancel tasks.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "outbreaksnearme.org",
        "/api/usersubmission/stats/region/NOA",
        "get",
        response=aresponses.Response(text=None, status=502),
    )
    aresponses.add(
        "outbreaksnearme.org",
        "/api/stats/US",
        "get",
        response=aresponses.Response(text=None, status=502),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)

        with pytest.raises(RequestError):
            _ = await client.user_data.async_get_totals()

    aresponses.assert_plan_strictly_followed()
