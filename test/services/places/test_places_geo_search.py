import pytest
import sqlmodel

import models
import services.places


@pytest.mark.skip(reason="minimize geo search requests")
def test_places_geo_search_chi(city_chi: models.City):
    assert city_chi.name == "chicago"

    code, geo_list = services.places.geo_search_by_name(box=city_chi, name="bavette bar and boeuf")

    assert code == 0
    assert len(geo_list) == 1
    assert geo_list[0].get("geometry").get("type") == "Point"
    assert geo_list[0].get("properties").get("name") == "Bavette's Bar & Boeuf"
    assert geo_list[0].get("properties").get("source_id")
    assert geo_list[0].get("properties").get("source_name") == "google"


def test_places_geo_search_tokyo(city_tokyo: models.City):
    assert city_tokyo.name == "tokyo"

    code, geo_list = services.places.geo_search_by_name(box=city_tokyo, name="boutique w")

    assert code == 0
    assert len(geo_list) == 1
    assert geo_list[0].get("geometry").get("type") == "Point"
    assert geo_list[0].get("properties").get("city") == "tokyo"
    assert geo_list[0].get("properties").get("lat")
    assert geo_list[0].get("properties").get("lon")
    assert geo_list[0].get("properties").get("name") == "boutiqueW"
    assert geo_list[0].get("properties").get("source_id")
    assert geo_list[0].get("properties").get("source_name") == "google"
