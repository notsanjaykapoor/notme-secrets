import json

import models
import services.crypto_keys.gpg

def test_gpg_encrypt(key_gpg_me: models.CryptoKey):
    data = {
        "user": "user@gmail.com",
        "password": "secret",
    }

    pgp_msg = services.crypto_keys.gpg.encrypt(key=key_gpg_me, plain_text=json.dumps(data))

    assert pgp_msg.startswith("-----BEGIN PGP MESSAGE-----")

    plain_text = services.crypto_keys.gpg.decrypt(key=key_gpg_me, pgp_msg=pgp_msg)
    plain_dict = json.loads(plain_text)

    assert plain_dict.get("user") == "user@gmail.com"
    assert plain_dict.get("password") == "secret"


