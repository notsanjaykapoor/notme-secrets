import sqlmodel

import models
import services.bookmarks
import services.bookmarks.categories


def test_bookmarks_categories_list(db_session: sqlmodel.Session, bm_1: models.Bookmark):
    assert bm_1.name == "bookmark-1"
    assert bm_1.categories == ["category-1"]

    cat_set = services.bookmarks.categories.list_all(db_session=db_session)

    assert cat_set == set(["category-1"])
