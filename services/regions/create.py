import re

import geoalchemy2.shape
import shapely.geometry
import sqlmodel

import models
import services.goog_geocode
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

    geo_features = services.goog_geocode.search_address(addr=name)

    if not geo_features:
        return 422, None

    if len(geo_features) != 1:
        return 422, None

    geo_json = geo_features[0]
    bbox = geo_json.get("bbox")

    geo_props = geo_json.get("properties", {})

    region_name = geo_props.get("name").lower()
    region_slug = re.sub(r"\s", "-", region_name)

    country_code = geo_props.get("country_code", "").lower()

    lat = geo_props.get("lat")
    lon = geo_props.get("lon")

    source_id = geo_props.get("source_id", "")
    source_name = geo_props.get("source_name", "")
    type = geo_props.get("result_type")

    geom_wkb = geoalchemy2.shape.from_shape(shapely.geometry.Point(lon, lat))

    # check region name again for uniqueness, the city search will normalize the name so its a good check here

    if region_db := services.regions.get_by_name(db_session=db_session, name=region_name):
        return 409, region_db

    region_db = models.Region(
        bbox=bbox,
        country_code=country_code,
        lat=lat,
        lon=lon,
        data={},
        geo_json=geo_json,
        geom_wkb=geom_wkb,
        name=region_name,
        slug=region_slug,
        source_id=source_id,
        source_name=source_name,
        type=type,
    )

    db_session.add(region_db)
    db_session.commit()

    return 0, region_db
