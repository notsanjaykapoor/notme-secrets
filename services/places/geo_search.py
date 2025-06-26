import os

import requests

import models


def geo_search_by_name(city: models.City, name: str) -> tuple[int, dict]:
    """
    Geo search place by name and location.
    """
    if city.country_code == "jp":
        geo_list = _google_search(city=city, query=name)
    else:
        geo_list = _geoapify_search(city=city, query=name, radius=10)

    return 0, geo_list


def _geoapify_search(city: models.City, query: str, radius: int) -> list[dict]:
    """
    Geoapify places search near a city.
    """
    geo_url = "https://api.geoapify.com/v1/geocode/search"

    geo_key = os.getenv("GEOAPIFY_KEY")

    meters = radius * 1609.34
    geo_params = {
        "apiKey": geo_key,
        "filter": f"circle:{city.lon},{city.lat},{meters}",
        "text": query
    }

    response = requests.get(geo_url, params=geo_params)
    data_json = response.json()

    if data_json.get("type") == "FeatureCollection":
        return data_json.get("features")
    
    return []


def _google_search(city: models.City, query: str) -> list[dict]:
    """
    Google places search near a city.

    docs: https://developers.google.com/maps/documentation/places/web-service/text-search
    """
    geo_url = "https://places.googleapis.com/v1/places:searchText"

    geo_key = os.getenv("GOOGLE_PLACES_KEY")

    geo_headers = {
        "X-Goog-Api-Key": geo_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types",
    }

    geo_query = f"{query} near {city.name}, {city.country_code}"

    geo_params = {
        "textQuery": geo_query,
    }

    response = requests.post(geo_url, headers=geo_headers, json=geo_params)
    data_json = response.json()
    places_list = data_json.get("places", [])

    # todo - map places dict into geo_json features

    return places_list
