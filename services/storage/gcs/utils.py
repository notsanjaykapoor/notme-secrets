import os

import services.secrets


def cache_dir() -> str:
    """
    """
    fs_uri= os.environ.get("SECRETS_FS_URI")
    _host, cache_dir, _ = services.secrets.file_uri_parse(source_uri=fs_uri)

    return cache_dir
