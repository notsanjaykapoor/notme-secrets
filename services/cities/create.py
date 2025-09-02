import re

import geoalchemy2.shape
import shapely.geometry
import sqlmodel

import models
import services.cities
import services.goog_geocode


def create(
    db_session: sqlmodel.Session,
    name: str,
    country_code: str = "",
) -> tuple[int, models.City | None]:
    """
    Create city and persist to database
    """
    name_norm = name.lower()

    city_db = services.cities.get_by_name(db_session=db_session, name=name_norm, country_code=country_code)

    if city_db:
        return 409, city_db

    if country_code:
        name_norm = f"{name_norm}, {country_code}"

    geo_features = services.goog_geocode.search_address(addr=name_norm)

    if not geo_features:
        return 422, None

    geo_json = geo_features[0]
    bbox = geo_json.get("bbox")

    geo_props = geo_json.get("properties", {})

    city_name = geo_props.get("name").lower()
    city_slug = re.sub(r"\s", "-", city_name)

    country_code = geo_props.get("country_code", "").lower()
    lat = geo_props.get("lat")
    lon = geo_props.get("lon")
    source_id = geo_props.get("source_id", "")
    source_name = geo_props.get("source_name")

    geom_wkb = geoalchemy2.shape.from_shape(shapely.geometry.Point(lon, lat))

    # check city name again for uniqueness, the city search will normalize the name so its a good check here

    if city_db := services.cities.get_by_name(db_session=db_session, name=city_name, country_code=country_code):
        return 409, city_db

    city_db = models.City(
        bbox=bbox,
        country_code=country_code,
        lat=lat,
        lon=lon,
        data={},
        geo_json=geo_json,
        geom=geom_wkb,
        name=city_name,
        slug=city_slug,
        source_id=source_id,
        source_name=source_name,
    )

    db_session.add(city_db)
    db_session.commit()

    return 0, city_db
