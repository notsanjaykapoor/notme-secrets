import sqlmodel

import models
import services.places.functions


def test_tool_call(db_session: sqlmodel.Session, city_chi: models.City, place_1: models.Place, mocker):
    assert place_1.tags == ["fashion"]

    mocker.patch("services.database.session.get", return_value=db_session)

    result_dict = services.places.functions.list_by_tags_city(city=city_chi.name, tags=["fashion"])

    assert result_dict["places"] == [place_1]
    assert result_dict["total"] == 1
