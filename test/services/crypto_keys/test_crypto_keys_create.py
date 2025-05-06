import pytest
import sqlalchemy.exc
import sqlmodel

import models
import services.crypto_keys
import services.database

def test_crypto_keys_create(db_session: sqlmodel.Session, user_1: models.User):
    # create with valid name and location
    key = services.crypto_keys.create(
        db_session=db_session,
        location="kms:projects/notme-xxx/locations/us-central1/keyRings/ring-1/cryptoKeys/key-symmetric",
        name="key-1",
        type=models.crypto_key.TYPE_KMS_SYM,
        user_id=user_1.id,
    )

    assert key.id
    assert key.location == "kms:projects/notme-xxx/locations/us-central1/keyRings/ring-1/cryptoKeys/key-symmetric"
    assert key.name == "key-1"
    assert key.type == "kms-sym"

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        # [name, user] should be unique
        services.crypto_keys.create(
            db_session=db_session,
            location="",
            name="key-1",
            type=models.crypto_key.TYPE_KMS_SYM,
            user_id=user_1.id,
        )

    db_session.rollback()

    services.database.truncate_tables(db_session=db_session, table_names=["crypto_keys"])

