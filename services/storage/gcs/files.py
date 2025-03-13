import dataclasses

import google.cloud.storage.blob

import services.storage.gcs


@dataclasses.dataclass
class FileGetStruct:
    code: int
    blob_name: str
    cache_dir: str
    cache_path: str
    errors: list[str]


def file_get(bucket_name: str, org_name: str, file_name: str) -> FileGetStruct:
    """
    """
    struct = FileGetStruct(
        code=0,
        blob_name="",
        cache_dir="",
        cache_path="",
        errors=[]
    )

    struct.blob_name = f"{org_name}/{file_name}"
    struct.cache_dir = f"{services.storage.gcs.cache_dir()}{org_name}/"
    struct.cache_path = f"{struct.cache_dir}{file_name}"

    services.storage.gcs.blob_download(bucket_name=bucket_name, blob_name=struct.blob_name, file_path_dst=struct.cache_path)

    return struct


def files_list(bucket_name: str, org_name: str) -> list[google.cloud.storage.blob.Blob]:
    """"
    List all files (blobs) in bucket 'bucket_name' under the top level folder (blob) 'org_name'.
    """
    org_prefix = f"{org_name}/"
    blobs_list = services.storage.gcs.blobs_list(bucket_name=bucket_name, prefix=org_prefix, delimiter="/")

    blobs_list = [blob for blob in blobs_list if blob.name != org_prefix]

    return blobs_list


