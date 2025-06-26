import os

import requests

import models


def get_by_id(goog_id: str) -> dict:  # noqa: F821
    """
    Google place details

    docs: https://developers.google.com/maps/documentation/places/web-service/place-details
    """
    geo_url = f"https://places.googleapis.com/v1/places/{goog_id}"
    geo_key = os.getenv("GOOGLE_PLACES_KEY")
    geo_headers = {
        "X-Goog-Api-Key": geo_key,
        "X-Goog-FieldMask": "displayName,location,name,shortFormattedAddress,types",
    }

    geo_params = {
        "languageCode": "en",
    }

    response = requests.get(geo_url, headers=geo_headers, params=geo_params)
    data_json = response.json()

    # map google data to geo_json format

    lat = data_json.get("location", {}).get("latitude")
    lon = data_json.get("location", {}).get("longitude")

    print(data_json) # xxx

    geo_json = {
        "type": "Feature",
        "geometry": {
            "coordinates": [lon, lat],
            "type": "Point",
        },
        "properties": {
            "address": data_json.get("shortFormattedAddress"),
            "goog": data_json, # raw data
            "lat": lat,
            "lon": lon,
            "name": data_json.get("displayName", {}).get("text", ""),
            "source_id": goog_id,
            "source_name": models.place.SOURCE_GOOGLE,
            "tags": data_json.get("types", []),
        },
    }

    return geo_json