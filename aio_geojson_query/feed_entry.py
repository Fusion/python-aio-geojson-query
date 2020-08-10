"""NSW Rural Fire Service Incidents feed entry."""
import pytz
import calendar
from datetime import datetime
from time import strptime

import logging
import re
from typing import Optional, Dict, Tuple
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import ATTRIBUTION, CUSTOM_ATTRIBUTE

_LOGGER = logging.getLogger(__name__)


class GeoJsonQueryEntry(FeedEntry):
    """NSW Rural Fire Service Incidents feed entry."""


    def __init__(self,
                 home_coordinates: Tuple[float, float],
                 feature: Feature,
                 mappings: Dict[str, str]):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)
        self._mappings = mappings


    @property
    def attribution(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return ATTRIBUTION


    @property
    def title(self) -> str:
        """Return the title of this entry."""
        title = self._parametric_search('title')
        if title: return title
        title = self._search_in_properties('title')
        if title: return title
        title = self._search_in_properties('details')
        if title: return title
        return None


    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        id = self._parametric_search('id')
        if id: return id
        id = self._search_in_properties('id')
        if id: return id
        id = self._search_in_properties('guid')
        if id: return id
        return None


    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        publication_date = self._parametric_search('date')
        if not publication_date:
            publication_date = self._search_in_properties('time')
        if not publication_date:
            publication_date = self._search_in_properties('date')
        if publication_date:
            # So, what kind of date are we facing?
            if self._mappings and 'dateformat' in self._mappings:
                date_format = self._mappings['dateformat']
                if date_format == 'seconds':
                    publication_date = datetime.fromtimestamp(publication_date)
                elif date_format == 'milliseconds':
                    publication_date = datetime.fromtimestamp(publication_date / 1000)
                else:
                # Parse the date. Example: 15/09/2018 9:31:00 AM
                    date_struct = strptime(publication_date, date_format)
                    publication_date = datetime.fromtimestamp(calendar.timegm(
                        date_struct), tz=pytz.utc)
            else:
                    date_struct = strptime(publication_date, "%d/%m/%Y %I:%M:%S %p")
                    publication_date = datetime.fromtimestamp(calendar.timegm(
                        date_struct), tz=pytz.utc)
        return publication_date


    def _parametric_search(self, search) -> str:
        if self._mappings and search in self._mappings:
            criteria = self._mappings[search]
            unpacked = criteria.split('~~', 1)
            if len(unpacked) > 1:
                varname, formula = unpacked
                value = self._search_in_properties(varname)
                match = re.search(formula.format(CUSTOM_ATTRIBUTE), value)
                if match:
                    return match.group(CUSTOM_ATTRIBUTE)
            else:
                varname = unpacked[0]
                return self._search_in_properties(varname)
        return None


    @property
    def description(self) -> str:
        description = self._parametric_search('description')
        if description: return description
        description = self._search_in_properties('description')
        if description: return description
        description = self._search_in_properties('details')
        if description: return description
        return None


    @property
    def location(self) -> str:
        """Return the location of this entry."""
        return self._parametric_search('location')


    @property
    def area(self) -> str:
        """Return the council area of this entry."""
        return self._parametric_search('area')


    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._parametric_search('status')


    @property
    def type(self) -> str:
        """Return the type of this entry."""
        return self._parametric_search('type')

    @property
    def size(self) -> str:
        """Return the size of this entry."""
        return self._parametric_search('size')

    @property
    def agency(self) -> str:
        """Return the responsible agency of this entry."""
        return self._parametric_search('agency')

    def criteria(self, name) -> str:
        return self._search_in_properties(name)
