import os
import shutil

import services.storage.gcs

def test_gcs_sync_download():
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

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == ["secret-1.txt"]
    assert len(sync_result.files_synced) == 1
    assert sync_result.files_synced == ["secret-1.txt"]
    assert sync_result.files_synced[0] in os.listdir(cache_org_dir)

    # mark synced file with an old version

    assert len(os.listdir(cache_org_dir)) == 2

    cache_file_version = sorted(os.listdir(cache_org_dir))[1] # should be secret-1.txt.version
    cache_path_cur = f"{cache_org_dir}{cache_file_version}"
    cache_path_new = f"{cache_org_dir}secret-1.txt.0000"

    os.rename(cache_path_cur, cache_path_new)

    # should resync all files in org-1

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_dirty == ["secret-1.txt"]
    assert len(sync_result.files_synced) == 1
    assert sync_result.files_synced == ["secret-1.txt"]
    assert sync_result.files_synced[0] in os.listdir(cache_org_dir)

    # should be idempotent

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_deleted == []
    assert sync_result.files_dirty == []
    assert len(sync_result.files_synced) == 0

    # should filter based on match_glob

    sync_result = services.storage.gcs.sync_download(
        bucket_name=bucket_name,
        org_name="org-1",
        cache_dir=cache_dir,
        sync_mode="rw",
        match_glob="secret-1.txt",
    )

    assert sync_result.files_checked == 1
    assert sync_result.files_deleted == []
    assert sync_result.files_dirty == []
    assert len(sync_result.files_synced) == 0

    sync_result = services.storage.gcs.sync_download(
        bucket_name=bucket_name,
        org_name="org-1",
        cache_dir=cache_dir,
        sync_mode="rw",
        match_glob="secret-2.txt",
    )

    assert sync_result.files_checked == 0
    assert sync_result.files_deleted == []
    assert len(sync_result.files_synced) == 0

    # should download blob to cache dir

    get_result = services.storage.gcs.file_get(bucket_name=bucket_name, org_name="org-1", file_name="secret-1.txt")

    assert get_result.blob_name == "org-1/secret-1.txt"
    assert get_result.cache_dir == cache_org_dir
    assert len(os.listdir(cache_org_dir)) == 2


def test_gcs_sync_upload():
    bucket_name = services.storage.gcs.bucket_name()

    assert bucket_name == "notme-secrets-tst"

    # should be 2 top level folders

    folder_names = services.storage.gcs.bucket_folders(bucket_name=bucket_name)

    assert folder_names == ["org-1", "org-2"]

    # clean cache dir

    cache_dir = services.storage.gcs.cache_dir()

    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    # create cache org dir

    cache_org_dir = f"{cache_dir}org-1/"

    os.makedirs(cache_org_dir, exist_ok=True)

    # create new secrets file, write xxx.gpg.new first, then xxx.gpg

    file_1 = open(f"{cache_org_dir}new-1.gpg.new", "w")
    file_1.close()

    # sync_download should not delete partial secrets file 

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_deleted == []
    assert "new-1.gpg" not in sync_result.files_dirty
    # assert sync_result.files_synced == []

    file_2 = open(f"{cache_org_dir}new-1.gpg", "w")
    file_2.close()

    #  the new secret .gpg and .new files should exist in local cache
    assert (set(["new-1.gpg", "new-1.gpg.new"]) - set(os.listdir(cache_org_dir))) == set()

    # sync_download should not delete new secrets file

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_deleted == []
    assert "new-1.gpg" not in sync_result.files_dirty
    # assert sync_result.files_synced == []

    # sync_upload should upload new secrets file

    sync_result = services.storage.gcs.sync_upload(cache_dir=cache_dir, bucket_name=bucket_name, org_name="org-1", sync_mode="w")

    assert sync_result.files_checked == 1
    assert sync_result.files_new == 1
    assert sync_result.files_synced == ["new-1.gpg"]

    # sync_upload should be idempotent

    sync_result = services.storage.gcs.sync_upload(cache_dir=cache_dir, bucket_name=bucket_name, org_name="org-1", sync_mode="w")

    assert sync_result.files_checked == 0
    assert sync_result.files_new == 0
    assert sync_result.files_synced == []

    # sync_download should ignore new file since its already synced

    sync_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name="org-1", cache_dir=cache_dir, sync_mode="r")

    assert sync_result.files_deleted == []
    assert "new-1.gpg" not in sync_result.files_dirty

    # cleanup gcs storage

    services.storage.gcs.blob_delete(bucket_name=bucket_name, blob_name="org-1/new-1.gpg")