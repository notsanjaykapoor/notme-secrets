import base64

import models
import services.crypto_keys.kms


def decrypt(key: models.CryptoKey, base64_text: str) -> str:
    """
    Decrypt base64 encoded cipher text with kms key.
    """
    client = services.crypto_keys.kms.client()

    # base64 to cipher bytes
    cipher_bytes = base64.b64decode(base64_text)

    decrypt_response = client.decrypt(
        request={
            "name": key.kms_name,
            "ciphertext": cipher_bytes,
        }
    )

    plain_bytes = decrypt_response.plaintext

    return plain_bytes.decode("utf-8")