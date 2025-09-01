import sqlmodel

import models
import services.crypto_keys


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.CryptoKey | None:
    """ """
    db_select = sqlmodel.select(models.CryptoKey).where(models.CryptoKey.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_id_user(
    db_session: sqlmodel.Session, id: int, user_id: int
) -> models.CryptoKey | None:
    """ """
    db_select = (
        sqlmodel.select(models.CryptoKey)
        .where(models.CryptoKey.id == id)
        .where(models.CryptoKey.user_id == user_id)
    )
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_name(db_session: sqlmodel.Session, name: str) -> models.CryptoKey | None:
    """ """
    db_select = sqlmodel.select(models.CryptoKey).where(models.CryptoKey.name == name)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_user_default(
    db_session: sqlmodel.Session, user_id: int
) -> models.CryptoKey | None:
    """ """
    list_result = services.crypto_keys.list(
        db_session=db_session,
        query=f"name:~default user_id:{user_id}",
        offset=0,
        limit=1,
    )

    if list_result.total != 1:
        return None

    return list_result.objects[0]
