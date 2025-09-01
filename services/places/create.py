import geoalchemy2.shape
import shapely.geometry
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
    
    bbox = geo_json.get("bbox", [])

    geo_props = geo_json.get("properties", {})
    country_code = city.country_code # geo_props.get("country_code", "").lower()
    source_id = geo_props.get("source_id", "") or geo_props.get("place_id", "")

    if "lat" in geo_props.keys():
        lat = geo_props.get("lat")
        lon = geo_props.get("lon")
    else:
        # get lat/lon from geometry
        lon, lat = geo_json.get("geometry", {}).get("coordinates", [0.0, 0.0])

    if datasource := geo_props.get("datasource", {}):
        source_name = datasource.get("sourcename", "")
    else:
        source_name = geo_props.get("source_name", "")

    geom_wkb = geoalchemy2.shape.from_shape(
        shapely.geometry.Point(lon, lat)
    )

    if place_db:
        # check place source to see if data is being updated
        if source_name == place_db.source_name:
            # same place and source
            return 409, place_db
        
        # place source is different, update place
        place_db.country_code = country_code
        place_db.geo_json = geo_json
        place_db.geom = geom_wkb
        place_db.lat = lat
        place_db.lon = lon
        place_db.source_id = source_id
        place_db.source_name = source_name

        db_session.add(place_db)
        db_session.commit()

        return 200, place_db

    # create new place

    place_db = models.Place(
        bbox=bbox,
        city=city.name,
        country_code=country_code,
        data={},
        geo_json=geo_json,
        geom=geom_wkb,
        lat=lat,
        lon=lon,
        name=name_norm,
        source_id=source_id,
        source_name=source_name,
        tags=[],
        user_id=user.id,
    )

    db_session.add(place_db)
    db_session.commit()

    return 0, place_db
