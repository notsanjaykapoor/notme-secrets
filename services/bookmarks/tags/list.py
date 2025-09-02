import sqlmodel

import models


def list_all(db_session: sqlmodel.Session):
    """
    Get set of all bookmark tags
    """
    dataset = sqlmodel.select(models.Bookmark.tags)
    db_result = db_session.exec(dataset).all()

    tags_set = set()

    for str_list in db_result:
        tags_set = tags_set.union(set(str_list))

    return tags_set


def list_by_categories(db_session: sqlmodel.Session, categories: list[str]):
    """
    Get set of all bookmark tags with any of the specified category tags.
    """
    dataset = sqlmodel.select(models.Bookmark.tags).where(models.Bookmark.categories.contains(categories))
    db_result = db_session.exec(dataset).all()

    tags_set = set()

    for str_list in db_result:
        tags_set = tags_set.union(set(str_list))

    return tags_set
