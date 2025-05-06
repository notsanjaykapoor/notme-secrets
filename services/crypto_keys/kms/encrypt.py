import base64

import services.crypto_keys.kms


def encrypt(key_name: str, plain_text: str) -> str:
    """ """
    client = services.crypto_keys.kms.client()

    encrypt_response = client.encrypt(
        request={
            "name": key_name,
            "plaintext": plain_text.encode("utf-8"),
        }
    )

    # encrypt_response.name has the key name with version used for encryption

    base64_text = base64.b64encode(encrypt_response.ciphertext).decode("utf-8")

    return base64_text