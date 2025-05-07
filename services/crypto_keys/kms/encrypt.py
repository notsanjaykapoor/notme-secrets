import base64

import models
import services.crypto_keys.kms


def encrypt(key: models.CryptoKey, plain_text: str) -> str:
    """
    Encrypt plain text with kms key and return base64 encoded cipher text.
    """
    client = services.crypto_keys.kms.client()

    encrypt_response = client.encrypt(
        request={
            "name": key.kms_name,
            "plaintext": plain_text.encode("utf-8"),
        }
    )

    # encrypt_response.name has the key name with version used for encryption

    base64_text = base64.b64encode(encrypt_response.ciphertext).decode("utf-8")

    return base64_text