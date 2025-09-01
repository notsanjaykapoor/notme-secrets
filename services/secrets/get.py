import sqlmodel

import models


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.Secret | None:
    """ """
    db_select = sqlmodel.select(models.Secret).where(models.Secret.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_id_user(
    db_session: sqlmodel.Session, id: int, user_id: int
) -> models.Secret | None:
    """ """
    db_select = (
        sqlmodel.select(models.Secret)
        .where(models.Secret.id == id)
        .where(models.Secret.user_id == user_id)
    )
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name_user(
    db_session: sqlmodel.Session, name: str, user_id: int
) -> models.Secret | None:
    db_select = (
        sqlmodel.select(models.Secret)
        .where(models.Secret.name == name)
        .where(models.Secret.user_id == user_id)
    )
    db_object = db_session.exec(db_select).first()

    return db_object
