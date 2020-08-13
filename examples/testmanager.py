import asyncio
from aiohttp import ClientSession
from aio_geojson_query import (GeoJsonQueryFeed, GeoJsonQueryFeedManager)


async def _generate_entity(external_id):
    print("Generate")


async def _update_entity(external_id):
    print("Update")


async def _remove_entity(external_id):
    print("Remove")


async def main() -> None:
    async with ClientSession() as websession:

        feed_manager = GeoJsonQueryFeedManager(
            websession,
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
            _generate_entity,
            _update_entity,
            _remove_entity,
            (34.052235, -118.243683),
            filter_radius=50,
            filter_criteria=None,
            mappings={
                "id": "code",
                "dateformat": "milliseconds",
                "date": "updated"
            }
        )

        status = await feed_manager.update()


asyncio.get_event_loop().run_until_complete(main())
