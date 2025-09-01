import pytest
import sqlalchemy.exc
import sqlmodel

import models
import services.bookmarks
import services.database


def test_bookmarks_create(db_session: sqlmodel.Session, user_1: models.User):
    # create with valid name and uri
    bm = services.bookmarks.create(
        db_session=db_session,
        categories=["cat-1"],
        name="bm-1",
        user_id=user_1.id,
        uri="https://www.notme.one",
    )

    assert bm.id
    assert bm.categories == ["cat-1"]
    assert bm.links == []
    assert bm.name == "bm-1"
    assert bm.tags == []
    assert bm.user_id == user_1.id
    assert bm.uri == "https://www.notme.one"

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        # name should be unique
        bm = services.bookmarks.create(
            db_session=db_session,
            name="bm-1",
            user_id=user_1.id,
            uri="https://www.notme.one",
        )

    db_session.rollback()

    # name should be lowercase
    bm = services.bookmarks.create(
        db_session=db_session,
        name="Bookmark 2",
        user_id=user_1.id,
        uri="https://www.notme.one",
    )

    assert bm.id
    assert bm.name == "bookmark 2"

    services.database.truncate_tables(db_session=db_session, table_names=["bookmarks"])
