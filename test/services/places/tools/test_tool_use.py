import sqlmodel

import models
import services.places.functions


def test_tool_use(db_session: sqlmodel.Session, city_chi: models.City, place_1: models.Place, mocker):
    assert place_1.tags == ["fashion"]

    mocker.patch("services.database.session.get", return_value=db_session)

    output_str = services.places.functions.list_by_tags_city(city=city_chi.name, tags=["fashion"])
    assert place_1.name in output_str
    assert place_1.city in output_str
