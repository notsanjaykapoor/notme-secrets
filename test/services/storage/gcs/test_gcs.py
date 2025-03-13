import os
import shutil

import services.storage.gcs

def test_gcs():
    bucket_name = services.storage.gcs.bucket_name()

    assert bucket_name == "notme-secrets-tst"

    # should be 2 top level folders

    folder_names = services.storage.gcs.bucket_folders(bucket_name=bucket_name)

    assert folder_names == ["org-1", "org-2"]

    # should be 1 file in org-1 folder

    blobs_list = services.storage.gcs.files_list(bucket_name=bucket_name, org_name="org-1")
    file_names = [blob.name for blob in blobs_list]

    assert file_names == ["org-1/secret-1.txt"]

    # clean cache dir

    cache_dir = services.storage.gcs.cache_dir()

    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    cache_org_dir = f"{cache_dir}org-1/"

    # should sync all files in org-1

    sync_result = services.storage.gcs.sync(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="rw")

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == 1
    assert len(sync_result.files_synced) == 2
    assert sync_result.files_synced[0] == "secret-1.txt"
    assert sync_result.files_synced[1].startswith("secret-1.txt.")
    assert os.listdir(cache_org_dir) == sync_result.files_synced

    file_name_version = sync_result.files_synced[1]

    # mark synced file with an old version

    cache_file = sync_result.files_synced[1]
    cache_path_cur = f"{cache_org_dir}{cache_file}"
    cache_path_new = f"{cache_org_dir}secret-1.txt.0000"

    os.rename(cache_path_cur, cache_path_new)

    # should resync all files in org-1

    sync_result = services.storage.gcs.sync(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="rw")

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == 1
    assert len(sync_result.files_synced) == 2
    assert sync_result.files_synced[0] == "secret-1.txt"
    assert sync_result.files_synced[1] == file_name_version # same version as before
    assert os.listdir(cache_org_dir) == sync_result.files_synced

    # should be idempotent

    sync_result = services.storage.gcs.sync(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="rw")

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == 0
    assert len(sync_result.files_synced) == 0

    # should filter based on match_glob

    sync_result = services.storage.gcs.sync(
        bucket_name=bucket_name,
        org_name="org-1",
        cache_dir=cache_dir,
        sync_mode="rw",
        match_glob="secret-1.txt",
    )

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == 0
    assert len(sync_result.files_synced) == 0

    sync_result = services.storage.gcs.sync(
        bucket_name=bucket_name,
        org_name="org-1",
        cache_dir=cache_dir,
        sync_mode="rw",
        match_glob="secret-2.txt",
    )

    assert sync_result.files_checked == 0
    assert len(sync_result.files_synced) == 0

    # should download blob to cache dir

    get_result = services.storage.gcs.file_get(bucket_name=bucket_name, org_name="org-1", file_name="secret-1.txt")

    assert get_result.blob_name == "org-1/secret-1.txt"
    assert get_result.cache_dir == cache_org_dir
    assert os.listdir(cache_org_dir) == ["secret-1.txt", file_name_version]