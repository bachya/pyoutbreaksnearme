"""Define dynamic fixtures."""
import json
from typing import Any, cast

import pytest

from tests.common import load_fixture


@pytest.fixture(name="markers_us_response", scope="session")
def markers_us_response_fixture() -> dict[str, Any]:
    """Define a fixture to return user report data.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("markers_us_response.json")))


@pytest.fixture(name="nonuserstats_us_response", scope="session")
def nonuserstats_us_response_fixture() -> dict[str, Any]:
    """Define a fixture to return CDC data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("nonuserstats_us_response.json"))
    )


@pytest.fixture(name="stats_us_response", scope="session")
def stats_us_response_fixture() -> dict[str, Any]:
    """Define a fixture to return user report totals per disease type.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("stats_us_response.json")))


@pytest.fixture(name="usersubmission_stats_region_noa_response", scope="session")
def usersubmission_stats_region_noa_response_fixture() -> dict[str, Any]:
    """Define a fixture to return the total number of user reports.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any],
        json.loads(load_fixture("usersubmission_stats_region_noa_response.json")),
    )
