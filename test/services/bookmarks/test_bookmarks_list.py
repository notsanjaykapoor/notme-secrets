import sqlmodel

import models
import services.bookmarks


def test_bookmarks_list_with_name_query(
    db_session: sqlmodel.Session, bm_1: models.Bookmark
):
    assert bm_1.name == "bookmark-1"

    # name match
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="name:bookmark",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 1
    assert list_result.total == 1

    # name match normalized
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="bookmark",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 1
    assert list_result.total == 1

    # name nomatch
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="name:foo",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 0
    assert list_result.total == 0


def test_bookmarks_list_with_tags_query(
    db_session: sqlmodel.Session, bm_1: models.Bookmark
):
    # tags match
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="tags:tag-1",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 1
    assert list_result.total == 1

    # tags partial match
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="tags:foo-1,tag-1",
        offset=0,
        limit=10,
    )

    # tags nomatch
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="tags:foo-1",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 0
    assert list_result.total == 0
