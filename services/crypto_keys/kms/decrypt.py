import base64
import time

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


def decrypt_with_time(key: models.CryptoKey, base64_text: str) -> tuple[str, float]:
    """
    Decrypt with timing info
    """
    t_start = time.time()
    text = decrypt(key=key, base64_text=base64_text)
    t_secs = round((time.time() - t_start), 1)

    return text, t_secs
