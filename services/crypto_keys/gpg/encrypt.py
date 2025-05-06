import models
import services.crypto_keys.gpg


def encrypt(key: models.CryptoKey, plain_text: str) -> str:
    """
    Encrypt text with gpg key
    """
    gpg, gpg_key = services.crypto_keys.gpg.gpg_key(gpg_dir=key.location)

    # crypt_struct is of type gnupg.Crypt
    crypt_struct = gpg.encrypt(data=plain_text, recipients=[gpg_key.get("fingerprint")])

    return crypt_struct.data.decode("utf-8")