"""Define user data."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, Dict, cast

from pyoutbreaksnearme.util.geo import haversine


class UserData:
    """Define a manager object for state/coordinate data."""

    def __init__(self, async_request: Callable[..., Awaitable[dict[str, Any]]]):
        """Initialize."""
        self._async_request = async_request

    async def async_get_nearest_by_coordinates(
        self, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """Get the nearest user reports to a latitude/longitude."""
        raw_user_report_data = await self._async_request("get", "markers/US")
        feature = min(
            raw_user_report_data["features"],
            key=lambda r: haversine(
                latitude,
                longitude,
                r["geometry"]["coordinates"][1],
                r["geometry"]["coordinates"][0],
            ),
        )
        return cast(Dict[str, Any], feature["properties"])

    async def async_get_totals(self) -> dict[str, Any]:
        """Get user report totals."""
        tasks = [
            self._async_request("get", "usersubmission/stats/region/NOA"),
            self._async_request("get", "stats/US"),
        ]
        results = await asyncio.gather(*tasks)
        return {**results[0], **results[1]}
