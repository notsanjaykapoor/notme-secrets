import sqlmodel

import models
import services.places

def create(
    db_session: sqlmodel.Session,
    user: models.User,
    city: models.City,
    geo_json: dict,
    name: str,
) -> tuple[int, models.Place | None]:
    """
    Create place and persist to database
    """
    name_norm = name.lower()

    place_db = services.places.get_by_name(db_session=db_session, name=name_norm)

    if place_db:
        return 409, place_db

    bbox = geo_json.get("bbox", [])

    geo_props = geo_json.get("properties", {})
    country_code = city.country_code # geo_props.get("country_code", "").lower()
    source_id = geo_props.get("place_id", "") or geo_props.get("source_id", "")

    if "lat" in geo_props.keys():
        lat = geo_props.get("lat")
        lon = geo_props.get("lon")
    else:
        # get lat/lon from geometry
        lon, lat = geo_json.get("geometry", {}).get("coordinates", [])

    if datasource := geo_props.get("datasource", {}):
        source_name = datasource.get("sourcename", "")
    else:
        source_name = geo_props.get("source_name", "")

    place_db = models.Place(
        bbox=bbox,
        city=city.name,
        country_code=country_code,
        lat=lat,
        lon=lon,
        data={},
        geo_json=geo_json,
        name=name_norm,
        source_id=source_id,
        source_name=source_name,
        user_id=user.id,
    )

    db_session.add(place_db)
    db_session.commit()

    return 0, place_db
