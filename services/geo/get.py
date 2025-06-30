import sqlmodel

import models


def get_by_name(db_session: sqlmodel.Session, name: str) -> models.City | models.Region | None:
    """
    Get geo object by name.

    Geo objects include cities and regions.
    """
    model_names = [models.City, models.Region]

    for model_name in model_names:
        db_select = sqlmodel.select(model_name).where(model_name.name == name.lower())
        db_object = db_session.exec(db_select).first()

        if db_object:
            return db_object

    return None


def get_by_slug(db_session: sqlmodel.Session, slug: str) -> models.City | models.Region | None:
    """
    Get geo object by name.

    Geo objects include cities and regions.
    """
    model_names = [models.City, models.Region]

    for model_name in model_names:
        db_select = sqlmodel.select(model_name).where(model_name.slug == slug)
        db_object = db_session.exec(db_select).first()

        if db_object:
            return db_object

    return None