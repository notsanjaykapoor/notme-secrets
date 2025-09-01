import google.cloud.kms


def client():
    return google.cloud.kms.KeyManagementServiceClient()
