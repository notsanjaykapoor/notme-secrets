import google.cloud.storage
import google.cloud.storage.bucket


def buckets_list() -> list[google.cloud.storage.bucket.Bucket]:
    client = google.cloud.storage.Client()
    return [b for b in client.list_buckets()]