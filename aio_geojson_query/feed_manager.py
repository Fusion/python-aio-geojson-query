"""Feed Manager for NSW Rural Fire Service Incidents feed."""
from typing import List, Dict, Tuple, Callable, Awaitable

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import GeoJsonQueryFeed


class GeoJsonQueryFeedManager(FeedManagerBase):

    def __init__(self,
                 websession: ClientSession,
                 endpoint: str,
                 generate_callback: Callable[[str], Awaitable[None]],
                 update_callback: Callable[[str], Awaitable[None]],
                 remove_callback: Callable[[str], Awaitable[None]],
                 coordinates: Tuple[float, float],
                 filter_radius: float = None,
                 filter_criteria: List[List[str]] = None,
                 mappings: Dict[str, str] = None,
                 status_callback: Callable[[StatusUpdate],
                                           Awaitable[None]] = None):
        """Initialize the NSW Rural Fire Services Feed Manager."""
        feed = GeoJsonQueryFeed(
            websession,
            endpoint,
            coordinates,
            filter_radius=filter_radius,
            filter_criteria=filter_criteria,
            mappings=mappings)
        super().__init__(feed,
                         generate_callback,
                         update_callback,
                         remove_callback,
                         status_async_callback=status_callback)
