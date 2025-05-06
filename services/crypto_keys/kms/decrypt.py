import base64

import services.crypto_keys.kms


def decrypt(key_name: str, base64_text: str) -> str:
    """ """
    client = services.crypto_keys.kms.client()

    # base64 to cipher bytes
    cipher_bytes = base64.b64decode(base64_text)

    decrypt_response = client.decrypt(
        request={
            "name": key_name,
            "ciphertext": cipher_bytes,
        }
    )

    plain_bytes = decrypt_response.plaintext

    return plain_bytes.decode("utf-8")