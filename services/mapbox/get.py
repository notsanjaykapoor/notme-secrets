import os

import requests
import ulid

import models


def get_by_id(mapbox_id: str, session_token: str = "") -> dict:
    """
    Get mapbox place

    docs: https://docs.mapbox.com/api/search/search-box/
    """
    endpoint = f"https://api.mapbox.com/search/searchbox/v1/retrieve/{mapbox_id}"

    api_token = os.getenv("MAPBOX_TOKEN")
    session_token = session_token or ulid.new().str

    params = {
        "access_token": api_token,
        "session_token": session_token,
    }

    response = requests.get(endpoint, params=params)
    data_json = response.json()

    if (data_type := data_json.get("type")) != "FeatureCollection":
        raise ValueError(f"type unexpected {data_type}")

    geo_json = data_json.get("features")[0]

    geo_json["properties"]["source_id"] = geo_json["properties"].get("mapbox_id")
    geo_json["properties"]["source_name"] = models.place.SOURCE_MAPBOX

    return geo_json
