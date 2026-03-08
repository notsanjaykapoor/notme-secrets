import pytest
import sqlmodel

import models
import services.places.tools
import services.places.tools.search


@pytest.mark.asyncio
async def test_tool_search_by_city(db_session: sqlmodel.Session, place_tokyo_1: models.Place, mocker):
    assert place_tokyo_1.brands == ["klasica"]
    assert place_tokyo_1.tags == ["fashion"]

    mocker.patch("services.database.session.get", return_value=db_session)

    result_obj = await services.places.tools.search.search_by_city(
        brands=["KLASICA", "Strange Brand"],
        ctx=None,
        city="tokyo",
        tags=["Fashion"],
    )

    # should normalize brands and tags, and find 1 place

    assert result_obj["places"] == [place_tokyo_1.as_dict()]
    assert result_obj["total"] == 1
