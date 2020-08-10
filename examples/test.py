import asyncio
from aiohttp import ClientSession
from aio_geojson_query import GeoJsonQueryFeed


async def main() -> None:
    async with ClientSession() as websession:
        # NSW Incidents Feed
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 50 km
        # Filter categories: 'Advice'
        feed = GeoJsonQueryFeed(websession,
                                "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json",
                                (-33.0, 150.0),
                                filter_radius=500,
                                filter_criteria=[
                                    ['category', '==', 'Advice']
                                    ],
                                mappings={
                                    "date": "pubDate",
                                    "location": "description~~LOCATION: (?P<{}>[^<]+) <br"
                                })
        status, entries = await feed.update()
        print(status)
        for entry in entries:
            print("%s [%s]: @%s" % (entry.title, entry.publication_date, entry.location))

        # Earthquakes, magnitude at least 3, around Los Angeles
        feed2 = GeoJsonQueryFeed(websession,
                                "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
                                (34.052235, -118.243683),
                                filter_criteria=[
                                    ['mag', '>', '3.0']
                                    ],
                                filter_radius=50,
                                mappings={
                                    "dateformat": "milliseconds",
                                    "date": "updated"
                                })
        status, entries = await feed2.update()
        print(status)
        for entry in entries:
            print("%s [%s]: @%s" % (entry.title, entry.publication_date, entry.title))


asyncio.get_event_loop().run_until_complete(main())
