import sqlmodel

import models
import services.places.tools


def test_places_match_tool_use():
    queries_match = ["find fashion in paris", "find fashion in france", "find brand calmlence in paris", "find brand calmlence in france", "search fashion in belgium"]

    for query in queries_match:
        code = services.places.tools.match_tool_use(query=query)
        assert code == 1


def test_places_tool(db_session: sqlmodel.Session, city_chi: models.City, place_1: models.Place):
    places_list = services.places.tools.list_by_tags_city(city=city_chi.name, tags=["fashion"])
    assert places_list
