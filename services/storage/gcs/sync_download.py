import dataclasses
import os
import re

import services.storage.gcs


@dataclasses.dataclass
class Struct:
    code: int
    files_checked: int
    files_deleted: list[str]
    files_dirty: list[str]
    files_synced: list[str]
    errors: list[str]


def sync_download(
    bucket_name: str,
    folder_name: str,
    cache_dir: str,
    sync_mode: str,
    match_glob: str = "",
) -> Struct:
    """
    Sync gcs bucket folder with local cache dir.


    """
    struct = Struct(
        code=0,
        files_checked=0,
        files_deleted=[],
        files_dirty=[],
        files_synced=[],
        errors=[],
    )

    if not cache_dir.endswith("/"):
        cache_dir = f"{cache_dir}/"

    # cache_folder_dir = f"{cache_dir}{folder_name}/"

    os.makedirs(cache_dir, exist_ok=True)

    cache_files_map = _cache_files_map(cache_files=os.listdir(cache_dir))
    cache_files_seen = []

    blobs_list = services.storage.gcs.files_list(bucket_name=bucket_name, folder_name=folder_name)

    for blob in blobs_list:
        secret_file = blob.name.split("/")[-1]
        secret_version = blob.generation

        if match_glob and not re.match(rf"{match_glob}", secret_file):
            cache_files_seen.append(secret_file)
            continue

        struct.files_checked += 1

        secret_file_version = f"{secret_file}.{secret_version}"

        cache_file_struct = cache_files_map.get(secret_file)

        if cache_file_struct and cache_file_struct.name == secret_file_version:
            # cache secret and version files are synced
            cache_files_seen.append(secret_file)
            continue

        struct.files_dirty.append(secret_file)

        if "w" in sync_mode:
            # secret is not cached, get gcs secret file
            _get_result = services.storage.gcs.file_download(
                bucket_name=bucket_name,
                folder_name=folder_name,
                file_name=secret_file,
                cache_dir=cache_dir,
            )

            cache_files_seen.append(secret_file)
            struct.files_synced.append(secret_file)

            # check for an old version file

            if cache_file_struct and cache_file_struct.name != secret_file_version:
                # secret version file is cached, but its old
                cache_file_old = cache_file_struct.name
                os.remove(f"{cache_dir}{cache_file_old}")

            # create cached secret version file
            file = open(f"{cache_dir}{secret_file_version}", "w")
            file.close()

    # check for deleted gcs secret files

    cache_files_del = set(cache_files_map.keys()) - set(cache_files_seen)

    if "w" in sync_mode and cache_files_del:
        for cache_file_secret in cache_files_del:
            cache_file_struct = cache_files_map.get(cache_file_secret)

            if cache_file_struct and cache_file_struct.type == "new":
                # cache secret and new file exist, this is a new secret that needs to be uploaded
                continue

            # find all related files and delete
            cache_files_del_list = [f for f in os.listdir(cache_dir) if f.startswith(cache_file_secret)]

            for cache_file in cache_files_del_list:
                os.remove(f"{cache_dir}{cache_file}")
                struct.files_deleted.append(cache_file)

    return struct


@dataclasses.dataclass
class FileStruct:
    name: str  # cache file name, e.g. x.gpg.1234, x.gpg.new
    type: str  # cache file type, e.g. new, version


def _cache_files_map(cache_files: list[str]) -> dict[str, FileStruct]:
    """ """
    files_map = {}

    for file in sorted(cache_files):
        if not re.search(r"(\.\d+)|(\.new)$", file):
            files_map[file] = FileStruct(name="", type="")
        else:
            file_root = re.sub(r"(\.\d+)|(\.new)$", "", file)
            if not (file_struct := files_map.get(file_root, None)):
                continue

            if file.endswith("new"):
                file_type = "new"
            else:
                file_type = "version"

            file_struct.name = file
            file_struct.type = file_type

    return files_map
