import dataclasses
import os
import re

import services.storage.gcs


@dataclasses.dataclass
class Struct:
    code: int
    files_checked: int
    files_new: int
    files_synced: list[str]
    errors: list[str]


def sync_upload(
    cache_dir: str,
    bucket_name: str,
    folder_name: str,
    sync_mode: str,
    match_glob: str = "",
) -> Struct:
    """
    Sync local secrets cache dir with gcs bucket.
    """
    struct = Struct(
        code=0,
        files_checked=0,
        files_new=0,
        files_synced=[],
        errors=[],
    )

    if not cache_dir.endswith("/"):
        cache_dir = f"{cache_dir}/"

    cache_org_dir = f"{cache_dir}/{folder_name}/"

    os.makedirs(cache_org_dir, exist_ok=True)

    cache_files_list = os.listdir(cache_org_dir)
    cache_files_list_new = [s for s in cache_files_list if s.endswith(".new")]

    blobs_list = services.storage.gcs.files_list(
        bucket_name=bucket_name, folder_name=folder_name
    )
    blobs_names = [blob.name.split("/")[-1] for blob in blobs_list]

    file_upload_list = []

    for cache_file_new in cache_files_list_new:
        struct.files_checked += 1

        # get raw gpp name, e.g. 'file.gpg.new' => 'file.gpg'
        cache_file_gpg = re.sub("\.new$", "", cache_file_new)

        if cache_file_gpg not in blobs_names:
            # found a new secrets file
            file_upload_list.append(cache_file_gpg)
            struct.files_new += 1

    if "w" in sync_mode:
        # upload new file(s)
        for cache_file_gpg in file_upload_list:
            cache_path_gpg = f"{cache_org_dir}{cache_file_gpg}"
            blob_name_dst = f"{folder_name}/{cache_file_gpg}"

            # upload blob to storage bucket
            services.storage.gcs.blob_upload(
                bucket_name=bucket_name,
                file_name_src=cache_path_gpg,
                blob_name_dst=blob_name_dst,
            )

            # get blob so we can get metadata
            blob = services.storage.gcs.blob_get(
                bucket_name=bucket_name, blob_name=blob_name_dst
            )

            # create cache version file
            cache_file_gpg_version = f"{cache_file_gpg}.{blob.generation}"
            file = open(f"{cache_org_dir}{cache_file_gpg_version}", "w")
            file.close()

            # delete .new file to mark file upload complete
            cache_file_gpg_new = f"{cache_file_gpg}.new"
            os.remove(f"{cache_org_dir}{cache_file_gpg_new}")

            struct.files_synced.append(cache_file_gpg)

    return struct
