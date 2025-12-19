import os

import models
import services.crypto_keys.gpg


def get_by_name(org: str, name: str) -> models.SecretData | None:
    dir_uri = os.environ["SECRETS_FS_URI"]
    source_host, source_dir, _ = services.crypto_keys.gpg.file_uri_parse(source_uri=dir_uri)

    file_path = f"{source_dir}{org}/{name}"

    if not file_path.endswith("gpg"):
        file_path = f"{file_path}.gpg"

    if not os.path.exists(file_path):
        return None

    secret_data = models.SecretData(name=name, path=file_path, uri=f"file://{source_host}/{file_path}")

    return secret_data
