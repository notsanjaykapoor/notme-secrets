import json

import pytest

import models
import services.crypto_keys.kms


@pytest.mark.skip(reason="encrypt methods time out in test env")
def test_kms_encrypt(key_kms_1: models.CryptoKey):
    assert key_kms_1.type == "kms-sym"

    data = {
        "user": "user@gmail.com",
        "password": "secret",
    }

    kms_base64 = services.crypto_keys.kms.encrypt(
        key=key_kms_1, plain_text=json.dumps(data)
    )

    # should return base64 encrypted string
    assert isinstance(kms_base64, str)

    plain_text = services.crypto_keys.kms.decrypt(key=key_kms_1, base64_text=kms_base64)
    plain_dict = json.loads(plain_text)

    assert plain_dict.get("user") == "user@gmail.com"
    assert plain_dict.get("password") == "secret"
