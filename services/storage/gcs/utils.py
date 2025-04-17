import os

import services.secrets


def cache_dir() -> str:
    """
    """
    _, cache_dir, _ = services.secrets.file_uri_parse(source_uri=os.environ.get("SECRETS_FS_URI"))

    return cache_dir

