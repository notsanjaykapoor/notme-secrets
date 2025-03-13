import asyncio

import services.storage.gcs

import context
import log

logger = log.init("app")

async def sync_task():
    """
    Sync all gcs orgs with local fs.

    This is run as a background task on app startup.
    """

    bucket_name = services.storage.gcs.bucket_name()
    cache_dir = services.storage.gcs.cache_dir()
    org_names = services.storage.gcs.bucket_folders(bucket_name=bucket_name)

    logger.info(f"{context.rid_get()} sync manager orgs '{org_names}', cache dir '{cache_dir}' starting")

    while True:
        for org in org_names:
            sync_result = services.storage.gcs.sync(bucket_name=bucket_name, org_name=org, cache_dir=cache_dir, sync_mode="rw")

            if sync_result.files_synced:
                logger.info(f"{context.rid_get()} sync manager org '{org}' - {len(sync_result.files_synced)} files synced")

        await asyncio.sleep(5)
