import sqlmodel

import models


def get_all_names_slugs(db_session: sqlmodel.Session) -> list[models.City]:
    db_select = sqlmodel.select(models.City.name, models.City.slug)
    db_select = db_select.order_by(models.City.name.asc())
    return db_session.exec(db_select).all()


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.City | None:
    """ """
    db_select = sqlmodel.select(models.City).where(models.City.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(db_session: sqlmodel.Session, name: str) -> models.City | None:
    """ """
    db_select = sqlmodel.select(models.City).where(models.City.name == name.lower())
    db_object = db_session.exec(db_select).first()

    return db_object
