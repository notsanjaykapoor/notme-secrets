import typing

import sqlmodel

import models


def get_by_id(db_session: sqlmodel.Session, id: int) -> typing.Optional[models.CryptoKey]:
    """ """
    db_select = sqlmodel.select(models.CryptoKey).where(models.CryptoKey.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(db_session: sqlmodel.Session, name: str) -> typing.Optional[models.CryptoKey]:
    """ """
    db_select = sqlmodel.select(models.CryptoKey).where(models.CryptoKey.name == name)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_user_default(db_session: sqlmodel.Session, user_id: int) -> typing.Optional[models.CryptoKey]:
    """ """
    db_select = sqlmodel.select(models.CryptoKey).where(models.CryptoKey.user_id == user_id)
    db_objects = db_session.exec(db_select).all()

    if len(db_objects) == 0:
        raise Exception("user has no keys")

    if len(db_objects) > 1:
        raise Exception("user has multiple keys")
    
    return db_objects[0]

