import asyncio

import services.storage.gcs

import context
import log
import models

logger = log.init("app")

# deprecated
async def sync_task(user: models.User):
    """
    Sync all gcs orgs with local fs.

    This is run as a background task on app startup.
    """

    bucket_name = services.storage.gcs.bucket_name(bucket_uri=user.bucket_uri)
    cache_dir = services.storage.gcs.cache_dir()
    org_names = services.storage.gcs.bucket_folders(bucket_name=bucket_name)

    logger.info(f"{context.rid_get()} sync manager user {user.id} bucket '{bucket_name}' orgs '{org_names}', cache dir '{cache_dir}' starting")

    sync_counter = 0

    while True:
        for org in org_names:
            # sync download - gcs changes to local fs
            download_result = services.storage.gcs.sync_download(bucket_name=bucket_name, org_name=org, cache_dir=cache_dir, sync_mode="rw")

            if download_result.files_synced:
                logger.info(f"{context.rid_get()} sync manager org '{org}' - files downloaded {len(download_result.files_synced)}")

            if download_result.files_deleted:
                logger.info(f"{context.rid_get()} sync manager org '{org}' - files deleted {len(download_result.files_deleted)}")

            if sync_counter % 5 == 0:
                # sync upload - local fs changes to gcs
                upload_result = services.storage.gcs.sync_upload(bucket_name=bucket_name, org_name=org, cache_dir=cache_dir, sync_mode="rw")

                if upload_result.files_synced:
                    logger.info(f"{context.rid_get()} sync manager org '{org}' - files uploaded {len(upload_result.files_synced)}")

            sync_counter += 1

        await asyncio.sleep(5)
