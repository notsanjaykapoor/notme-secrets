import os
import unicodedata

import requests

import models


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
    country_code = ""
    region_name = ""

    for addr_component in addr_components:
        if "country" in addr_component.get("types", []):
            country_code = addr_component.get("short_name", "").lower()

        if "locality" in addr_component.get("types", []):
            region_name = _region_remove_accents(
                name = addr_component.get("long_name", "").lower()
            )

    if not region_name:
        # try 'administrative_area_level_1' component
        if "administrative_area_level_1" in addr_component.get("types", []):
            region_name = _region_remove_accents(
                name = addr_component.get("long_name", "").lower()
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
            "bounds": addr_bounds,
            "country_code": country_code,
            "lat": lat,
            "lon": lon,
            "name": region_name,
            "source_id": addr.get("place_id"),
            "source_name": models.place.SOURCE_GOOGLE,
            "viewport": addr_viewport,
        },
    }

    return feature


def _region_bbox(bbox_object: dict) -> dict:
    return [
        bbox_object.get("southwest", {}).get("lng"),
        bbox_object.get("southwest", {}).get("lat"),
        bbox_object.get("northeast", {}).get("lng"),
        bbox_object.get("northeast", {}).get("lat"),    
    ]


def _region_remove_accents(name=str) -> str:
    """
    Removes accent marks (diacritics) from a Unicode string.
    """
    # Normalize the string to NFD (Normalization Form Canonical Decomposition)
    # This separates base characters from their combining diacritical marks.
    nfkd_form = unicodedata.normalize('NFKD', name)

    # Filter out characters that are combining diacritical marks ('Mn' category)
    # and join the remaining characters to form the new string.
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
