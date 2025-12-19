import os

import gnupg

import services.crypto_keys.gpg

# deprecated
def encrypt(password: str, user: str = "") -> gnupg.Crypt:
    """ """
    gpg, gpg_key = services.crypto_keys.gpg.gpg_key(gpg_dir=os.environ["GPG_HOME_URI"])

    data = [password]

    if user:
        data.append(f"user: {user}")

    crypt_struct = gpg.encrypt(data="\n".join(data), recipients=[gpg_key.get("fingerprint")])

    return crypt_struct
