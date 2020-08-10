import logging
from typing import List, Optional, Tuple, Dict
from datetime import datetime

from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
from geojson import FeatureCollection

from .feed_entry import GeoJsonQueryEntry

from functools import reduce

_LOGGER = logging.getLogger(__name__)


class GeoJsonQueryFeed(
        GeoJsonFeed[GeoJsonQueryEntry]):

    def __init__(self,
                 websession: ClientSession,
                 endpoint: str,
                 home_coordinates: Tuple[float, float],
                 filter_radius: float = None,
                 filter_criteria: List[List[str]] = None,
                 mappings: Dict[str, str] = None):
        """Initialise this service."""
        super().__init__(websession,
                         home_coordinates,
                         endpoint,
                         filter_radius=filter_radius)
        self._filter_criteria = filter_criteria
        self._mappings = mappings

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={}, criteria={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius, self._filter_criteria)

    def _new_entry(self, home_coordinates: Tuple[float, float], feature,
                   global_data: Dict) -> GeoJsonQueryEntry:
        """Generate a new entry."""
        return GeoJsonQueryEntry(home_coordinates, feature, self._mappings)

    # TODO Allow for 'and' filters -- at this time, these are 'or' only
    # TODO At this point, this is a bit confusing because our gt/lt tests
    # end up being inclusive(!)
    def _filter_entries(self,
                        entries: List[GeoJsonQueryEntry]) \
            -> List[GeoJsonQueryEntry]:

        def _compare(v1, v2, op):
            if op == '==':
                return v1 == v2
            elif op == '!=':
                return v1 != v2
            elif op == '>':
                return float(v1) > float(v2)
            elif op == '<':
                return float(v1) < float(v2)
            else:
                return False # TODO

        """Filter the provided entries."""
        filtered_entries = super()._filter_entries(entries)
        if self._filter_criteria:
            filtered_entries = list(filter(lambda entry:
                                    reduce((lambda truthiness, filter:
                                                truthiness or _compare(entry.criteria(filter[0]), filter[2], filter[1])),
                                             self._filter_criteria,
                                             False),
                                    filtered_entries))
        return filtered_entries

    def _extract_last_timestamp(
            self,
            feed_entries: List[GeoJsonQueryEntry]) \
            -> Optional[datetime]:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(filter(
                None, [entry.publication_date for entry in feed_entries]),
                reverse=True)
            return dates[0]
        return None

    def _extract_from_feed(self, feed: FeatureCollection) -> Optional[Dict]:
        """Extract global metadata from feed."""
        return None
