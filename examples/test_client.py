"""Test client functionality."""
import asyncio
import logging

from aiohttp import ClientSession

from pyoutbreaksnearme import Client
from pyoutbreaksnearme.errors import OutbreaksNearMeError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        logging.basicConfig(level=logging.DEBUG)

        client = Client(session=session)
        try:
            nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
                39.7251035, -104.99918
            )
            _LOGGER.info("Nearest user data: %s", nearest_user_data)

            user_totals_data = await client.user_data.async_get_totals()
            _LOGGER.info("User data totals: %s", user_totals_data)

            nearest_cdc_data = await client.cdc_data.async_get_nearest_by_coordinates(
                39.7251035, -104.99918
            )
            _LOGGER.info("Nearest CDC data: %s", nearest_cdc_data)
        except OutbreaksNearMeError as err:
            _LOGGER.error(err)


asyncio.run(main())
