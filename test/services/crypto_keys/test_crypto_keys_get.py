import sqlmodel

import models
import services.crypto_keys


def test_crypto_keys_get(db_session: sqlmodel.Session, user_1: models.User, key_kms_1: models.CryptoKey, key_gpg_1: models.CryptoKey):
    assert key_kms_1.name == "kms-1"
    assert key_gpg_1.name == "gpg-1"

    # user default key should return 0 matches because there are no keys with "default" in the name

    key_db = services.crypto_keys.get_user_default(
        db_session=db_session,
        user_id=user_1.id,
    )

    assert key_db == None

    # change key name

    key_kms_1.name = "user-default"
    db_session.add(key_kms_1)
    db_session.commit()

    # user default key should return a match

    key_db = services.crypto_keys.get_user_default(
        db_session=db_session,
        user_id=user_1.id,
    )

    assert key_db == key_kms_1

