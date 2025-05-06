import typing

import sqlmodel

import models


def create(
    db_session: sqlmodel.Session,
    data_cipher: str,
    key_id: int,
    name: str,
    user_id: int,
) -> typing.Optional[models.Secret]:
    """
    Create secret and persist to database
    """
    secret_db = models.Secret(
        data={},
        data_cipher=data_cipher,
        key_id=key_id,
        name=name.lower().strip(),
        user_id=user_id,
    )

    db_session.add(secret_db)
    db_session.commit()

    return secret_db
