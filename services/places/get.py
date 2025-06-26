import sqlmodel

import models


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.Place | None:
    """ """
    db_select = sqlmodel.select(models.Place).where(models.Place.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(db_session: sqlmodel.Session, name: str) -> models.Place | None:
    """ """
    db_select = sqlmodel.select(models.Place).where(models.Place.name == name)
    db_object = db_session.exec(db_select).first()

    return db_object
