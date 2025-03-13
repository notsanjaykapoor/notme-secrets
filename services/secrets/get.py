import os

import models
import services.secrets


def get_by_name(org: str, name: str) -> models.Secret | None:
    dir_uri= os.environ.get("SECRETS_FS_URI")
    source_host, source_dir, _ = services.secrets.file_uri_parse(source_uri=dir_uri)

    file_path = f"{source_dir}{org}/{name}"

    if not file_path.endswith("gpg"):
        file_path = f"{file_path}.gpg"

    if not os.path.exists(file_path):
        return None
    
    secret = models.Secret(
        name=name,
        path=file_path,
        uri=f"file://{source_host}/{file_path}"
    )

    return secret