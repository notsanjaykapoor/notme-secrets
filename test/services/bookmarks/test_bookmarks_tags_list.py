import sqlmodel

import models
import services.bookmarks
import services.bookmarks.tags


def test_bookmarks_tags_list(db_session: sqlmodel.Session, bm_1: models.Bookmark):
    assert bm_1.name == "bookmark-1"
    assert bm_1.categories == ["category-1"]
    assert bm_1.tags == ["tag-1"]

    tag_set = services.bookmarks.tags.list_all(db_session=db_session)

    assert tag_set == set(["tag-1"])

    tag_set = services.bookmarks.tags.list_by_categories(db_session=db_session, categories=["category-1"])

    assert tag_set == set(["tag-1"])

    tag_set = services.bookmarks.tags.list_by_categories(db_session=db_session, categories=["category-0"])

    assert tag_set == set([])