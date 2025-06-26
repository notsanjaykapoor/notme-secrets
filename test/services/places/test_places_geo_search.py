import sqlmodel

import models
import services.places


def test_places_geo_search_chi(db_session: sqlmodel.Session, city_chi: models.City):
    assert city_chi.name == "chicago"

    code, geo_list = services.places.geo_search_by_name(city=city_chi, name="bavette bar and boeuf")

    assert code == 0
    assert len(geo_list) == 1
    assert geo_list[0].get("geometry").get("type") == "Point"
    assert geo_list[0].get("properties").get("name") == "Bavette's Bar and Boeuf"
    assert geo_list[0].get("properties").get("source_id")
    assert geo_list[0].get("properties").get("source_name") == "mapbox"
    # assert geo_list[0].get("properties").get("datasource").get("sourcename") == "openstreetmap"

def test_places_geo_search_tokyo(db_session: sqlmodel.Session, city_tokyo: models.City):
    assert city_tokyo.name == "tokyo"

    code, geo_list = services.places.geo_search_by_name(city=city_tokyo, name="boutique w")

    assert code == 0
    assert len(geo_list) == 1
    assert geo_list[0].get("geometry").get("type") == "Point"
    assert geo_list[0].get("properties").get("name") == "boutiqueW"
    assert geo_list[0].get("properties").get("source_id")
    assert geo_list[0].get("properties").get("source_name") == "google"
