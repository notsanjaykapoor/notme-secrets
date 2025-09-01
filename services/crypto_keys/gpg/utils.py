import re

import gnupg


def file_uri_parse(source_uri: str) -> tuple[str, str, str]:
    """
    Parse a file uri into its component parts.

    example file uri - file:///users/notme/foo/bar.txt is parsed into components:

    path - /users/notme/foo/bar.txt
    dir - /users/notme/foo/
    file - bar.txt
    """
    if not (match := re.match(r"^file:\/\/(\/.+)$", source_uri)):
        raise ValueError(f"invalid source_uri {source_uri}")

    source_path = match[1]

    match = re.match(r"^(.+)\/([^\/]*)$", source_path)
    source_dir = f"{match[1]}/"
    source_file = match[2]

    return source_path, source_dir, source_file


def gpg_get(gpg_dir: str) -> gnupg.GPG:
    """
    get gpg object from directory
    """
    _, source_dir, _ = file_uri_parse(source_uri=gpg_dir)

    return gnupg.GPG(gnupghome=source_dir)


def gpg_key(gpg_dir: str) -> tuple[gnupg.GPG, dict]:
    """
    get gpg key from directory
    """
    gpg = gpg_get(gpg_dir=gpg_dir)

    return (gpg, gpg.list_keys()[0])
