"""Test client functionality."""
import asyncio
import logging
import os

from aiohttp import ClientSession

from pyoutbreaksnearme import Client
from pyoutbreaksnearme.errors import OutbreaksNearMeError

_LOGGER = logging.getLogger()

LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        logging.basicConfig(level=logging.INFO)

        client = Client(session=session)
        try:
            nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
                LATITUDE, LONGITUDE
            )
            _LOGGER.info("Nearest user data: %s", nearest_user_data)

            user_totals_data = await client.user_data.async_get_totals()
            _LOGGER.info("User data totals: %s", user_totals_data)
        except OutbreaksNearMeError as err:
            _LOGGER.error(err)


asyncio.run(main())
