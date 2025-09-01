import google.cloud.kms


def key_name(
    client, project_id: str, location_id: str, key_ring_id: str, key_id: str
) -> str:
    """
    Get kms key name from its components.

    params:
        client: Google Cloud client object
        project_id: Google Cloud project ID (e.g. 'my-project').
        location_id: Cloud KMS location (e.g. 'us-east1').
        key_ring_id: ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id: ID of the key to use (e.g. 'my-key').
    """
    return client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
