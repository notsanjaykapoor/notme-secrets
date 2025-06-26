import os
import re

import requests
import sqlmodel

import models
import services.cities

def create(
    db_session: sqlmodel.Session,
    name: str,
) -> tuple[int, models.City | None]:
    """
    Create city and persist to database
    """
    name_norm = name.lower()

    city_db = services.cities.get_by_name(db_session=db_session, name=name_norm)

    if city_db:
        return 409, city_db

    geo_params = {
        "apiKey": os.getenv("GEOAPIFY_KEY"),
        "text": name,
    }
    geo_url = "https://api.geoapify.com/v1/geocode/search"

    response = requests.get(geo_url, params=geo_params)
    data_json = response.json()
    
    if (type := data_json.get("type")) != "FeatureCollection":
        raise ValueError(f"unknown type {type}")

    # filter features for region types
    geo_features = data_json.get("features", [])
    geo_features = [feature for feature in geo_features if feature.get("properties", {}).get("result_type") in ["city"]]

    geo_json = geo_features[0]
    bbox = geo_json.get("bbox")

    geo_props = geo_json.get("properties", {})
    country_code = geo_props.get("country_code", "").lower()
    lat = geo_props.get("lat")
    lon = geo_props.get("lon")
    slug = re.sub(r"\s", "-", name_norm)
    source_id = geo_props.get("place_id", "")
    source_name = geo_props.get("datasource", {}).get("sourcename", "")

    city_db = models.City(
        bbox=bbox,
        country_code=country_code,
        lat=lat,
        lon=lon,
        data={},
        geo_json=geo_json,
        name=name_norm,
        slug=slug,
        source_id=source_id,
        source_name=source_name,
    )

    db_session.add(city_db)
    db_session.commit()

    return 0, city_db


