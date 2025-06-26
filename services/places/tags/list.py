import sqlmodel

import models


def list_all(db_session: sqlmodel.Session):
    """
    Get set of all places tags
    """
    dataset = sqlmodel.select(models.Place.tags)
    db_result = db_session.exec(dataset).all()

    tags_set = set()

    for str_list in db_result:
        tags_set = tags_set.union(set(str_list))

    return tags_set

