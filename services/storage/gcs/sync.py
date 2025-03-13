import dataclasses
import os
import re

import services.storage.gcs

@dataclasses.dataclass
class Struct:
    code: int
    files_checked: int
    files_dirty: int
    files_synced: list[str]
    errors: list[str]


def sync(bucket_name: str, org_name: str, cache_dir: str, sync_mode: str, match_glob: str="") -> Struct:
    """
    Sync gcs bucket/org with local cache dir. 
    """
    struct = Struct(
        code=0,
        files_checked=0,
        files_dirty=0,
        files_synced=[],
        errors=[],
    )

    if not cache_dir.endswith("/"):
        cache_dir = f"{cache_dir}/"

    cache_dir = f"{cache_dir}/{org_name}/"

    os.makedirs(cache_dir, exist_ok=True)

    cache_files_list = os.listdir(cache_dir)

    blobs_list = services.storage.gcs.files_list(bucket_name=bucket_name, org_name=org_name)

    for blob in blobs_list:
        secret_file = blob.name.split("/")[-1]
        secret_version = blob.generation

        if match_glob and not re.match(rf"{match_glob}", secret_file):
            continue

        struct.files_checked += 1

        cache_version = f"{secret_file}.{secret_version}"

        if cache_version in cache_files_list:
            # cache secret and version files are synced
            continue

        struct.files_dirty += 1

        if sync_mode == "rw":
            # get secret file
            _get_result = services.storage.gcs.file_get(bucket_name=bucket_name, org_name=org_name, file_name=secret_file)
            struct.files_synced.append(secret_file)

            # check for an old version file
            cache_files_filtered = [s for s in cache_files_list if s.startswith(f"{secret_file}.")]

            if cache_files_filtered:
                cache_file_old = cache_files_filtered[0]
                os.remove(f"{cache_dir}{cache_file_old}")

            # create cache version file
            file = open(f"{cache_dir}{cache_version}", "w")
            file.close()

            struct.files_synced.append(cache_version)

    return struct