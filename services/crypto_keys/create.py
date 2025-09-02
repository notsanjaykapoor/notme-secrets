import typing

import sqlmodel

import models


def create(
    db_session: sqlmodel.Session,
    location: str,
    name: str,
    type: str,
    user_id: int,
) -> typing.Optional[models.CryptoKey]:
    """
    Create crypto_key and persist to database
    """
    key_db = models.CryptoKey(
        location=location,
        name=name.lower().strip(),
        type=type,
        user_id=user_id,
    )

    db_session.add(key_db)
    db_session.commit()

    return key_db


def create_default(db_session: sqlmodel.Session, user_id: int) -> typing.Optional[models.CryptoKey]:
    """
    Create default crypto key
    """
    create(
        db_session=db_session,
        location=models.crypto_key.LOCATION_DEFAULT,
        name=models.crypto_key.NAME_DEFAULT,
        type=models.crypto_key.TYPE_GPG_SYM,
        user_id=user_id,
    )
