from getpass import getpass
import os


def repo_config():
    """
    Configure the repo to download models, weight, addons from that server
    """
    endpoint = input("S3 Endpoint:")
    access_key = input("S3 Access key:")
    secret_key = getpass("S3 Secret key:")
    with open(".secret", "w") as f:
        f.write(endpoint.strip())
        f.write("\n")
        f.write(access_key)
        f.write("\n")
        f.write(secret_key)


def read_secret():
    """
    Read credentials and informations of our repo

    Returns:
        (str, str, str, str, bool): endpoint, access_key, secret_key, secure of the
        repo that is configured
    """
    if not os.path.exists(".secret"):
        return 's3.amazonaws.com', \
               '', \
               '', \
               'eu-central-1', \
               True
    with open(".secret", "r") as f:
        endpoint = f.readline().strip()
        access_key = f.readline().strip()
        secret_key = f.readline().strip()
        region = f.readline().strip()
        secure = True if endpoint.startswith("https") else False
        endpoint = endpoint.replace("http://", "").replace("https://",
                                                           "").strip()
    return endpoint, access_key, secret_key, region, secure
