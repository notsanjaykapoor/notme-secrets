import sqlmodel

import models


def list_all(db_session: sqlmodel.Session):
    """
    Get set of all place brands
    """
    dataset = sqlmodel.select(models.Place.brands)
    db_result = db_session.exec(dataset).all()

    brands_set = set()

    for str_list in db_result:
        brands_set = brands_set.union(set(str_list))

    return brands_set


def list_by_box_tags(
    db_session: sqlmodel.Session,
    box: models.City | models.Region | None,
    tags: list[str],
):
    """
    Get set of all place brands, scoped by places with specified tags and city.
    """
    dataset = sqlmodel.select(models.Place.brands).where(
        models.Place.tags.contains(tags)
    )

    if box:
        dataset = dataset.where(models.Place.city == box.name)

    db_result = db_session.exec(dataset).all()

    brands_set = set()

    for str_list in db_result:
        brands_set = brands_set.union(set(str_list))

    return brands_set
