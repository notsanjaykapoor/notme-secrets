import os

import requests

import models
import services.goog_places


def search_address(addr: str) -> list[dict]:
    """
    Google geocoding service mapping names to coordinates

    docs: https://developers.google.com/maps/documentation/geocoding/start
    """
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_params = {
        "address": addr,
        "key": os.getenv("GOOGLE_PLACES_KEY"),
    }

    response = requests.get(geo_url, params=geo_params)
    data_json = response.json()
    results_list = data_json.get("results", [])

    # map address objects dict into geo_json features
    features_list = [_google_addr_to_feature(addr=addr_dict) for addr_dict in results_list]

    return features_list


def _google_addr_to_feature(addr: dict) -> dict:
    """
    Transform google address object into a geojson feature object.
    """
    addr_geom = addr.get("geometry", {})

    addr_bounds = addr_geom.get("bounds", {})
    addr_viewport = addr_geom.get("viewport", {})

    bbox = _region_bbox(bbox_object=addr_viewport or addr_bounds)

    lat = addr_geom.get("location", {}).get("lat")
    lon = addr_geom.get("location", {}).get("lng")

    address_formatted = addr.get("formatted_address", "")

    # parse address components into city name and country code
    addr_components = addr.get("address_components", [])
    country_code, city_name, locality, area = services.goog_places.address_components_city_country(
        addr_components=addr_components
    )

    feature = {
        "type": "Feature",
        "bbox": bbox,
        "geometry": {
            "coordinates": [lon, lat],
            "type": "Point",
        },
        "properties": {
            "address": address_formatted,
            "area": area,
            "bounds": addr_bounds,
            "country_code": country_code,
            "lat": lat,
            "lon": lon,
            "locality": locality,
            "name": city_name,
            "source_id": addr.get("place_id"),
            "source_name": models.place.SOURCE_GOOGLE,
            "viewport": addr_viewport,
        },
    }

    return feature


def _region_bbox(bbox_object: dict) -> tuple[float, float, float, float]:
    return bbox_object.get("southwest", {}).get("lng"), bbox_object.get("southwest", {}).get("lat"), bbox_object.get("northeast", {}).get("lng"), bbox_object.get("northeast", {}).get("lat")

