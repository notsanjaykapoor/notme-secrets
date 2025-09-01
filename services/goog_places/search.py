import os

import requests

import models
import services.goog_places


def search_by_city(city: models.City, query: str) -> list[dict]:
    """
    Google places search near a city.

    docs: https://developers.google.com/maps/documentation/places/web-service/text-search
    """
    geo_url = "https://places.googleapis.com/v1/places:searchText"
    geo_key = os.getenv("GOOGLE_PLACES_KEY")
    geo_headers = {
        "X-Goog-Api-Key": geo_key,
        "X-Goog-FieldMask": "places.addressComponents,places.displayName,places.shortFormattedAddress,places.id,places.location,places.types",
    }

    geo_query = f"{query} near {city.name}, {city.country_code}"
    geo_params = {
        "textQuery": geo_query,
    }

    response = requests.post(geo_url, headers=geo_headers, json=geo_params)
    data_json = response.json()
    places_list = data_json.get("places", [])

    # map places dict into geo_json features
    features_list = [_google_place_to_feature(place=place_dict) for place_dict in places_list]

    return features_list


def _google_place_to_feature(place: dict) -> dict:
    """
    Transform google place object into a geojson feature object.
    """
    place_types = place.get("types", [])  # e.g. 'point_of_interest', 'store'
    place_location = place.get("location", {})

    lat = place_location.get("latitude")
    lon = place_location.get("longitude")

    address = place.get("shortFormattedAddress", "")
    name = place.get("displayName", {}).get("text")

    country, city, locality, area = services.goog_places.address_components_city_country(addr_components=place.get("addressComponents", []))

    feature = {
        "type": "Feature",
        "geometry": {
            "coordinates": [lon, lat],
            "type": "Point",
        },
        "properties": {
            "address": address,
            "area": area,
            "city": city,
            "country": country,
            "lat": lat,
            "lon": lon,
            "locality": locality,
            "name": name,
            "source_id": place.get("id"),
            "source_name": models.place.SOURCE_GOOGLE,
            "tags": place_types,
        },
    }

    return feature
