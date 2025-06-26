import os
import re

import requests
import sqlmodel

import models
import services.regions

def create(
    db_session: sqlmodel.Session,
    name: str,
) -> tuple[int, models.Region | None]:
    """
    Create region and persist to database
    """
    name_norm = name.lower()

    region_db = services.regions.get_by_name(db_session=db_session, name=name_norm)

    if region_db:
        return 409, region_db

    geo_params = {
        "apiKey": os.getenv("GEOAPIFY_KEY"),
        "limit": 10,
        "text": name,
    }
    geo_url = "https://api.geoapify.com/v1/geocode/search"

    response = requests.get(geo_url, params=geo_params)
    data_json = response.json()
    
    if (type := data_json.get("type")) != "FeatureCollection":
        raise ValueError(f"unknown type {type}")

    geo_features = data_json.get("features", [])

    # filter features for region types
    geo_features = [feature for feature in geo_features if feature.get("properties", {}).get("result_type") in ["country"]]

    if len(geo_features) != 1:
        return 422, None
    
    geo_json = geo_features[0]
    bbox = geo_json.get("bbox")

    geo_props = geo_json.get("properties", {})
    country_code = geo_props.get("country_code", "").lower()
    lat = geo_props.get("lat")
    lon = geo_props.get("lon")
    slug = re.sub(r"\s", "-", name_norm)
    source_id = geo_props.get("place_id", "")
    source_name = geo_props.get("datasource", {}).get("sourcename", "")
    type = geo_props.get("result_type")

    region_db = models.Region(
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
        type=type,
    )

    db_session.add(region_db)
    db_session.commit()

    return 0, region_db


