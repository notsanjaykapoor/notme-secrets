import google.cloud.storage
import google.cloud.storage.blob


def blob_download(bucket_name: str, blob_name_src: str, file_name_dst: str):
    """
    Downloads a blob from the bucket.
    """
    client = google.cloud.storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name_src)
    blob.download_to_filename(file_name_dst)

    return 0


def blob_upload(bucket_name: str, file_name_src: str, blob_name_dst: str) -> int:
    """
    Uploads a file to the bucket.
    """
    client = google.cloud.storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name_dst) or bucket.blob(blob_name_dst)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.

    if blob:
        generation_match_val = blob.generation
    else:
        generation_match_val = 0

    blob.upload_from_filename(file_name_src, if_generation_match=generation_match_val)

    return generation_match_val


def blobs_list(bucket_name: str, prefix: str, delimiter: str=None) -> list[google.cloud.storage.blob.Blob]:
    """"
    Lists all the blobs in the bucket that begin with the prefix.

    The delimiter argument can be used to restrict the results to only the "files" in the given "folder".
    Without the delimiter, the entire tree under the prefix is returned. For example, given these blobs:

        a/1.txt
        a/b/2.txt

    If you specify prefix ='a/', without a delimiter, you'll get back:

        a/1.txt
        a/b/2.txt

    If you specify prefix='a/' and delimiter='/', you'll get back only the file directly under 'a/':

        a/1.txt

    As part of the response, you'll also get back a blobs.prefixes entity
    that lists the "subfolders" under `a/`:

        a/b/
    """

    client = google.cloud.storage.Client()
    blobs = client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)
    return [b for b in blobs]