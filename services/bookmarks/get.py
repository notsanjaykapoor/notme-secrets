import typing

import sqlmodel

import models


def get_by_id(
    db_session: sqlmodel.Session, id: int
) -> typing.Optional[models.Bookmark]:
    """ """
    db_select = sqlmodel.select(models.Bookmark).where(models.Bookmark.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(
    db_session: sqlmodel.Session, name: str
) -> typing.Optional[models.Bookmark]:
    """ """
    db_select = sqlmodel.select(models.Bookmark).where(models.Bookmark.name == name)
    db_object = db_session.exec(db_select).first()

    return db_object
