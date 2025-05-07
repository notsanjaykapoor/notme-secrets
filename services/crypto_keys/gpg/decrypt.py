import time

import models
import services.crypto_keys.gpg


def decrypt(key: models.CryptoKey, pgp_msg: str) -> str:
    """
    Decrypt pgp message with gpg key
    """
    gpg = services.crypto_keys.gpg.gpg_get(gpg_dir=key.location)

    decrypted_data = gpg.decrypt(pgp_msg)
    plain_text = str(decrypted_data)

    return plain_text


def decrypt_with_time(key: models.CryptoKey, pgp_msg: str) -> tuple[str, float]:
    """
    Decrypt with timing info
    """
    t_start = time.time()
    text = decrypt(key=key, pgp_msg=pgp_msg)
    t_secs = round((time.time() - t_start), 1)

    return [text, t_secs]
