import yaml
from minio import Minio, S3Error

from vsdkx.cli.credential import read_secret
from vsdkx.cli.global_constants import NAME_REGEX, POSTFIX_MODEL
import re, os

from vsdkx.cli.util import install, create_folder, modify_app, uninstall
from vsdkx.cli.weight import download_weight, remove_weight


def add_model(args):
    endpoint, access_key, secret_key, secure = read_secret()
    model = args[0]
    print(f"Adding model {model} ...")
    assert re.match(NAME_REGEX, model), \
        "model name is not right"
    install(f"vsdkx-model-{model}")
    create_folder("vsdkx")
    create_folder("vsdkx/model")
    current_profile = "vsdkx/model/profile.yaml"
    bucket_name = f"{model}{POSTFIX_MODEL}"
    minio = Minio(endpoint, access_key, secret_key, secure=secure)
    try:
        response = minio.get_object(bucket_name, "profile.yaml")
        dict1 = yaml.full_load(response)
        dict2 = {}
        if os.path.exists(current_profile):
            with open(current_profile, "r") as file:
                dict2 = yaml.full_load(file)
        if dict2 is None:
            dict2 = {}
        merged = {**dict1, **dict2}
        with open(current_profile, 'w') as file:
            yaml.dump(merged, file)
        modify_app(f"model-{model}")
        print(f"{model} added")
        download_weight(args)
    except S3Error as e:
        print(e)


def remove_model(args):
    model = args[0]
    uninstall(f"vsdkx-model-{model}")
    current_profile = "vsdkx/model/profile.yaml"
    if os.path.exists(current_profile):
        with open(current_profile, "r") as file:
            data = yaml.full_load(file)
            data.pop(model)
        if data is not None:
            with open(current_profile, "w") as file:
                yaml.dump(data, file)
    modify_app(f"model-{model}", True)
    remove_weight(args)
