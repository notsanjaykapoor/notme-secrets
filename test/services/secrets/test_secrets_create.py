import base64

import pytest
import sqlalchemy.exc
import sqlmodel

import models
import services.secrets
import services.database


def test_secrets_create(db_session: sqlmodel.Session, user_1: models.User, key_kms_1: models.CryptoKey):
    # create valid secret
    secret_db = services.secrets.create(
        db_session=db_session,
        data_cipher=base64.b64encode("plain text".encode("utf-8")),
        key_id=key_kms_1.id,
        name="key-1",
        user_id=user_1.id,
    )

    assert secret_db.id
    assert secret_db.key_id == key_kms_1.id
    assert secret_db.name == "key-1"
    assert secret_db.user_id == user_1.id

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        # [name, user] should be unique
        services.secrets.create(
            db_session=db_session,
            data_cipher="",
            key_id=key_kms_1.id,
            name="key-1",
            user_id=user_1.id,
        )

    db_session.rollback()

    services.database.truncate_tables(db_session=db_session, table_names=["secrets"])
