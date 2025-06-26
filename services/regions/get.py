import sqlmodel

import models


def get_all_names_slugs(db_session: sqlmodel.Session) -> list[models.Region]:
    db_select = sqlmodel.select(models.Region.name, models.Region.slug)
    return db_session.exec(db_select).all()


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.Region | None:
    """ """
    db_select = sqlmodel.select(models.Region).where(models.Region.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(db_session: sqlmodel.Session, name: str) -> models.Region | None:
    """ """
    db_select = sqlmodel.select(models.Region).where(models.Region.name == name.lower())
    db_object = db_session.exec(db_select).first()

    return db_object
