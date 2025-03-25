import sqlmodel

import models


def list_all(db_session: sqlmodel.Session):
    """
    Get set of all bookmark categories
    """
    dataset = sqlmodel.select(models.Bookmark.categories)
    db_result = db_session.exec(dataset).all()

    cats_set = set()

    for str_list in db_result:
        cats_set = cats_set.union(set(str_list))

    return cats_set