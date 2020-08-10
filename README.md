# python-aio-geojson-query

This library is my attempt at creating a generalized client for the [aio-geojson-client](https://github.com/exxamalte/python-aio-geojson-client) library.

Of course, this requires some uncomfortable contorting as the properties in a GeoJson feed are free-form (see [rfc7946](https://tools.ietf.org/html/rfc7946))

This is currently under development, so apologies for the bugs.

## Installation
`pip install aio-geojson-query`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supplying the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

### Status Codes

* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

### Parameters

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

#### Supported Filters

| Filter   |                   | Description                                                  |
| -------- | ----------------- | ------------------------------------------------------------ |
| Radius   | `filter_radius`   | Radius in kilometers around the home coordinates in which events from feed are included. |
| Criteria | `filter_criteria` | Array of filtering conditions.                               |

#### Criteria Syntax

At this time, criteria are pretty simple and are applied using an `or`operator. Therefore, properties matching any function will be a match.

Available operators are: `==`, `!=`, `<`, `>`.

The latter two will always compare the property as a float value.

### Mappings

Since this library has no knowledge of the feeds being retrieved, this is used to map property names. Mappings are passed as an additional argument called, of course, `mappings`

#### Mapping Names

By default, mappings are as simple as: the first argument is known, in the feed, as the second argument.

For instance, let's say you are looking for the `date` mapping and, in the feed, that field is called `published_date` -- you will want to help the library find it by passing this mapping:

`"date": "published_date"`

#### Parametric Mapping

Sometimes, a value can only be extracted from a complex property. For instance, `location` may only be available inside the `description` property. These mappings are denoted using `~~` followed by the regular expression that will extract the value:

`"location": "description~~LOCATION: (?P<{}>[^<]+) <br"`

#### Mandatory and default mappings

Some properties are mandatory. For instance, if the library does not find the `date` property, it will not be able to synchronize the feed properly.

If you do not specify mappings for these variables, the library may attempt to guess what their names could be.

For instance:

| Property      |                  | Guessed Names                              |
| ------------- | ---------------- | ------------------------------------------ |
| `date`        | Mandatory        | `time`, `date`                             |
| `dateformat`  | A pseudo mapping | Helps the library parse the date property. |
| `description` |                  | `description`, `details`                   |

#### Date Parsing

The `dateformat` pseudo mapping can be:

| Format              |      | Meaning                                         |
| ------------------- | ---- | ----------------------------------------------- |
| `seconds`           |      | This is an epoch timestamp,                     |
| `milliseconds`      |      | A timestamp in milliseconds.                    |
| An arbitrary string |      | Used by the library in the `strptime` function. |

## Example

I recommend checking out [python-aio-geojson-nsw-rfs-incidents](https://github.com/exxamalte/python-aio-geojson-nsw-rfs-incidents) which is a library dedicated to retrieving fire incidents information, written by the same author as the library I am creating this middleware for. You may be interested in comparing that library's example code to the one below, which does the same thing (then checks for earthquakes when done):

```python
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
```


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
