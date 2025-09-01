import os

import requests

import models


def search_by_city(city: models.City, query: str, radius: int) -> list[dict]:
    """
    Geoapify places search near a city.
    """
    geo_url = "https://api.geoapify.com/v1/geocode/search"

    geo_key = os.getenv("GEOAPIFY_KEY")

    meters = radius * 1609.34
    geo_params = {"apiKey": geo_key, "filter": f"circle:{city.lon},{city.lat},{meters}", "text": query}

    response = requests.get(geo_url, params=geo_params)
    data_json = response.json()

    if data_json.get("type") == "FeatureCollection":
        return data_json.get("features")

    return []
