import dataclasses
import glob
import os
import re

import models
import services.secrets


@dataclasses.dataclass
class Struct:
    code: int
    file_uris: list[str]
    objects: list[models.SecretData]
    errors: list[str]


def list(org: str, query: str, offset: int, limit: int) -> Struct:
    """
    list org password store files
    """
    struct = Struct(
        code=0,
        file_uris=[],
        objects=[],
        errors=[],
    )

    dir_uri= os.environ.get("SECRETS_FS_URI")
    source_host, source_dir, _ = services.secrets.file_uri_parse(source_uri=dir_uri)

    files = sorted(
        glob.glob(f"{source_dir}{org}/*.gpg", recursive=True)
    )

    for file in files:
        match = re.match(rf"({source_dir})(.+)\.gpg", file)
        file_name = match[2] # e.g. notme/goog, without the .gpg extension

        if org:
            file_name = file_name.replace(f"{org}/", "", 1) # strip org from file_name, notme/goog become goog

        if not query or query.lower() in file_name.lower():
            file_uri = f"file://{source_host}/{file}"

            passw = models.SecretData(
                name=file_name,
                path=file,
                uri=file_uri,
            )
            struct.objects.append(passw)
            struct.file_uris.append(file_uri)

    return struct
