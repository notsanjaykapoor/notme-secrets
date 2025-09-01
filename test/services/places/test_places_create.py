import sqlmodel
import ulid

import models
import services.database
import services.places


def test_places_create(
    db_session: sqlmodel.Session, user_1: models.User, city_chi: models.City
):
    # example geo search result

    geo_json = {
        "bbox": [],
        "properties": {
            "country_code": "us",
            "lat": city_chi.lat_f,
            "lon": city_chi.lon_f,
            "place_id": ulid.new().str,
        },
    }

    code, place_db = services.places.create(
        db_session=db_session,
        user=user_1,
        city=city_chi,
        geo_json=geo_json,
        name="Place 1",
    )

    assert code == 0
    assert place_db.id
    assert place_db.lat == city_chi.lat
    assert place_db.lon == city_chi.lon
    assert place_db.name == "place 1"
    assert place_db.point.x == place_db.lon_f
    assert place_db.point.y == place_db.lat_f
    assert place_db.source_id

    # create with duplicate name should return 409

    code, place_dup = services.places.create(
        db_session=db_session,
        user=user_1,
        city=city_chi,
        geo_json=geo_json,
        name="Place 1",
    )

    assert code == 409
    assert place_dup.id == place_db.id

    services.database.truncate_tables(db_session=db_session, table_names=["places"])
