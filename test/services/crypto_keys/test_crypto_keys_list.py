import sqlmodel

import models
import services.crypto_keys


def test_crypto_keys_list(
    db_session: sqlmodel.Session,
    key_kms_1: models.CryptoKey,
    key_gpg_1: models.CryptoKey,
):
    assert key_kms_1.name == "kms-1"
    assert key_gpg_1.name == "gpg-1"

    # name match
    list_result = services.crypto_keys.list(
        db_session=db_session,
        query="name:kms",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 1
    assert list_result.total == 1
    assert list_result.objects == [key_kms_1]

    # type match
    list_result = services.crypto_keys.list(
        db_session=db_session,
        query=f"type:{models.crypto_key.TYPE_GPG_SYM}",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 1
    assert list_result.total == 1
    assert list_result.objects == [key_gpg_1]

    # name nomatch
    list_result = services.bookmarks.list(
        db_session=db_session,
        query="name:foo",
        offset=0,
        limit=10,
    )

    assert list_result.code == 0
    assert list_result.count == 0
    assert list_result.total == 0
