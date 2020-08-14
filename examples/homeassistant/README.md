# What

Create entities based on any geojson source, allowing you to filter these sources in your maps, tables, etc.

For instance, you could display side-by-side a map of earthquakes and a map of wildfires (that is if you are lucky enough to live in California!)

# Setup

You need to clone this folder to '{config path}/custom_components'.
The commands below should create the correct hierarchy while not downloading the whole code, yet allowing you to upgrade.

```
git clone --depth=1 git@github.com:Fusion/python-aio-geojson-query.git --no-checkout
cd python-aio-geojson-query
git checkout master -- examples/homeassistant
ln -s $(pwd)/examples/homeassistant ../aio_geo_json_events
```

Add the geolocation source to `configuration.yaml`, or whichever configuration file you use for this purpose: 

```
geo_location:
  ...
  - platform: aio_geojson_query
    source: source_name
    endpoint: endpoint_url
    latitude: your_latitude
    longitude: your_longitude
    radius: desired_radius_in_km
    criteria:
      - your_criteria
    mappings:
      id: id_field_name
      dateformat: date_format
      date: date_field_name
    extra_fields:
      - extra_field_1
      - ...
      - extra_field_n
    entity_namespace: 'whatever_you_want'      
```

| Parameter                     |                                                              |
| ----------------------------- | ------------------------------------------------------------ |
| source_name                   | Short string that will be used to filter this unique source of geo events. |
| endpoint_url                  | Your GeoJson feed.                                           |
| your_latitude, your_longitude | If omitted, your home coordinates will be used.              |
| desired_radius_in_km          | Self explanatory.                                            |
| your_criteria                 | e.g. `mag > 4.0`                                             |
| id_field_name, etc.           | To parse your feed correctly. See the [main README file](https://github.com/Fusion/python-aio-geojson-query/blob/master/README.md). |

You can use this newly created source in e.g. Lovelace components such as `Map`:

```
- type: map
  geo_location_sources:
    - aio_geo_myquakes
```

This source (`aio_geo_myquakes`) was created by the component by concatenating the prefix `aio_geo_` with the source name  you selected above (here: `myquakes`) -- the prefix acts as a "name mangling" namespace.