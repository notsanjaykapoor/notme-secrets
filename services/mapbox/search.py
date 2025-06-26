import os

import requests
import ulid

import models

# docs: https://docs.mapbox.com/api/search/search-box/
# docs: https://docs.mapbox.com/api/search/search-box/#interactive-search
# docs: https://docs.mapbox.com/api/search/search-box/#search-request
# docs: https://docs.mapbox.com/api/search/search-box/#reverse-lookup

def search_by_city(city: models.City, query: str, limit: int=10) -> list[dict]:
    """
    Mapbox places search near a city.
    """
    api_token = os.getenv("MAPBOX_TOKEN")
    city_proximity = f"{city.lon},{city.lat}"

    endpoint = "https://api.mapbox.com/search/searchbox/v1/suggest"

    params = {
        "access_token": api_token,
        "q": query,
        "language": "en",
        "limit": limit,
        "proximity": city_proximity,
        "session_token": ulid.new().str, # required for suggest endpoint
        "types": "poi",
    }

    response = requests.get(endpoint, params=params)
    data_json = response.json()
    places_list = data_json.get("suggestions", [])

    # map places dict into geo_json features
    features_list = [_mapbox_place_to_feature(place=place_dict) for place_dict in places_list]

    return features_list


def _mapbox_place_to_feature(place: dict) -> dict:
    """
    Transform mapbox place object into a geojson feature object.
    """
    category_names = place.get("poi_category_ids", [])
    source_id = place.get("mapbox_id")
    source_name = models.place.SOURCE_MAPBOX

    feature = {
        "type": "Feature",
        "geometry": {
            "coordinates": [], # not lat, lon in these objects
            "type": "Point",
        },
        "properties": place | {
            "source_id": source_id,
            "source_name": source_name,
            "tags": category_names,
        },
    }

    return feature
