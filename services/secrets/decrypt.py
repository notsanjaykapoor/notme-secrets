import os
import re

import models
import services.crypto_keys.gpg


# deprecated
def decrypt(secret: models.SecretData) -> models.SecretData:
    """
    decrypt secret object using gpg key
    """
    gpg = services.crypto_keys.gpg.gpg_get(gpg_dir=os.environ["GPG_HOME_URI"])

    decrypted_data = gpg.decrypt_file(open(secret.path, "rb"))
    plaintext = str(decrypted_data)

    passw, *other = plaintext.split("\n")
    other = [s for s in other if s]

    secret.passw = passw

    if other and re.search(r"^(email:|id.*:|user.*:)", other[0]):
        secret.user = other[0].split(":")[1].strip()
    else:
        secret.user = ""

    return secret
