import os

import models
import services.secrets


def user_cache_dir(user: models.User, env: str) -> str:
    """
    Return user specific cache_dir location.
    """
    return f"{_cache_dir(env=env)}/user-{user.id}"


def _cache_dir(env: str) -> str:
    """ """
    if env in ["tst", "test"]:
        return f"{os.getcwd()}/test/data/cache"
    else:
        return f"{os.getcwd()}/data/cache"

    # _, cache_dir, _ = services.secrets.file_uri_parse(source_uri=os.environ.get("SECRETS_FS_URI"))

    # return cache_dir
