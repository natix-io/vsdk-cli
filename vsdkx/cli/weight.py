from minio import Minio, S3Error
import re, os, yaml
from vsdkx.cli.credential import read_secret
from vsdkx.cli.global_constants import POSTFIX_MODEL, NAME_REGEX
from vsdkx.cli.util import create_folder


def download_weight(args):
    """
    Downloads weight file from repo

    Args:
        args: args[0] is the model name and args[1] is the weight file name
    """
    endpoint, access_key, secret_key, region, secure = read_secret()
    model = args[0]
    weight: str = args[1] if len(args) > 1 else None
    if weight is not None:
        print(f"Downloading {weight} ...")
        bucket_name = f"{model}{POSTFIX_MODEL}"
        minio = Minio(endpoint, access_key, secret_key, region= region,
                      secure=secure)
        create_folder("vsdkx/weight")
        path = f"vsdkx/weight/{weight}"
        assert re.match(NAME_REGEX, weight), \
            "Weight name is not right"
        try:
            minio.fget_object(bucket_name, weight, path)

            current_profile = "vsdkx/model/profile.yaml"
            if os.path.exists(current_profile):
                with open(current_profile, "r") as file:
                    data = yaml.full_load(file)
                if data is not None:
                    with open(current_profile, "w") as file:
                        if data.get(model) is not None:
                            data[model][
                                "model_path"] = f"vsdkx/weight/{weight}"
                            yaml.dump(data, file)
            print(f"{weight} downloaded")
        except S3Error as e:
            print(e)


def remove_weight(args):
    """
    Removes weight file from current project

    Args:
        args: args[1] is the weight file name
    """
    weight = args[1] if len(args) > 1 else None
    print(f"Removing weight {weight} ...")
    if weight is not None:
        path = f"vsdkx/weight/{weight}"
        if os.path.exists(path):
            os.remove(path)
    print(f"{weight} removed")