import os
import re

import models
import services.secrets


def decrypt(secret: models.Secret) -> models.Secret:
    """
    decrypt password object using gpg key
    """
    gpg = services.secrets.gpg_get(gpg_dir=os.environ.get("GPG_HOME_URI"))

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

