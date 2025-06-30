import sqlmodel

import services.cities
import services.database

def test_cities_create(db_session: sqlmodel.Session):
    code, city_db = services.cities.create(db_session=db_session, name="Chicago")

    assert code == 0
    assert city_db.country_code == "us"
    assert city_db.data == {}
    assert city_db.geo_json
    assert city_db.lat_f == 41.88325
    assert city_db.lon_f == -87.6323879
    assert city_db.name == "chicago"
    assert city_db.slug == "chicago"
    assert city_db.source_id
    assert city_db.source_name == "google"
    assert city_db.tags == []

    code, city_dup = services.cities.create(db_session=db_session, name="Chicago")

    assert code == 409
    assert city_dup.id == city_db.id

    services.database.truncate_tables(db_session=db_session, table_names=["cities"])
