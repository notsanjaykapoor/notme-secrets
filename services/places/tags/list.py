import sqlmodel

import models


def list_all(db_session: sqlmodel.Session, box: models.City | models.Region | None):
    """
    Get set of all places tags, optionally filter by a city.
    """
    dataset = sqlmodel.select(models.Place.tags)

    if box:
        if box.type == models.box.TYPE_CITY:
            dataset = dataset.where(models.Place.city == box.name)
        else:
            dataset = dataset.where(models.Place.country_code.in_(box.country_codes))

    db_result = db_session.exec(dataset).all()

    tags_set = set()

    for str_list in db_result:
        tags_set = tags_set.union(set(str_list))

    return tags_set
