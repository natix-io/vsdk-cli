import argparse, argcomplete, os, shutil
from getpass import getpass
import re
from minio import Minio, S3Error
import yaml
import subprocess
import sys

POSTFIX_MODEL = "-product"
NAME_REGEX = "^([A-Za-z0-9\-.:])+$"

manifest = {
    "vsdkx-model-yolo-torch": "git+https://gitlab+deploy-token-488362:aQbEo4kAqEhppoUe3Tyh@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-torch",
    "vsdkx-model-yolo-tflite": "git+https://gitlab+deploy-token-488360:bRkGozdPs1yUjjLQS4Zy@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-tflite",
    "vsdkx-model-yolo-facemask": "git+https://gitlab+deploy-token-488359:fhs2HLs2ZHLxSvPHbt84@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-mask",
    "vsdkx-model-bayesian": "git+https://gitlab+deploy-token-488354:wfv9ruzXiDj93Dw6wrmP@gitlab.com/natix/cvison/vsdkx/vsdkx-model-bayesian",
    "vsdkx-model-resnet": "git+https://gitlab+deploy-token-488358:QVhHopKVuY4MWMyCNDEa@gitlab.com/natix/cvison/vsdkx/vsdkx-model-resnet",
    "vsdkx-model-mobilenet": "git+https://gitlab+deploy-token-488355:bRf2y6xyhHjQZrUy_uzB@gitlab.com/natix/cvison/vsdkx/vsdkx-model-mobilenet",
    "vsdkx-addon-distanti": "git+https://gitlab+deploy-token-488346:fjijyZBz2gStuv46anZs@gitlab.com/natix/cvison/vsdkx/vsdkx-addon-distant",
    "vsdkx-addon-facemask": "git+https://gitlab+deploy-token-488347:XxHx9VLvb7W4Ch1rnLt8@gitlab.com/natix/cvison/vsdkx/vsdkx-addon-facemask",
    "vsdkx-addon-tracking": "git+https://gitlab+deploy-token-488350:1jt8j5EcWg5gfvRF4Bq1@gitlab.com/natix/cvison/vsdkx/vsdkx-addon-tracking",
    "vsdkx-addon-zoning": "git+https://gitlab+deploy-token-488351:AaSywFKwJxPzv2qnFUia@gitlab.com/natix/cvison/vsdkx/vsdkx-addon-zoning"
}


def modify_requirement(package, remove=False):
    lines = []
    skip = False
    requirements = "requirements.txt"
    if os.path.exists(requirements):
        with open(requirements, "r") as file:
            for l in file:
                line = l.strip()
                if not line.startswith(package):
                    lines.append(line)
                else:
                    if not remove:
                        skip = True
                        break
    if not skip:
        if remove and not os.path.exists(requirements):
            return
        with open(requirements, "w") as file:
            for l in lines:
                file.write(l)
                file.write("\n")
            if not remove:
                file.write(package)
                file.write("\n")


def install(package):
    if manifest.get(package) is not None:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               manifest[package]])
        modify_requirement(package)
    else:
        print(f"No package {package} found")


def uninstall(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall",
                               package])
        modify_requirement(package, True)
    except:
        pass


def config():
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
    assert os.path.exists(".secret"), "You should run config first"
    with open(".secret", "r") as f:
        endpoint = f.readline().strip()
        access_key = f.readline().strip()
        secret_key = f.readline().strip()
        secure = True if endpoint.startswith("https") else False
        endpoint = endpoint.replace("http://", "").replace("https://",
                                                           "").strip()
    return endpoint, access_key, secret_key, secure


def create_folder(path):
    if not os.path.exists:
        os.mkdir(path)


def clean_all():
    if os.path.exists("vsdkx"):
        shutil.rmtree("vsdkx", True)


def download_weight(args):
    endpoint, access_key, secret_key, secure = read_secret()
    model = args[0]
    weight: str = args[1] if len(args) > 1 else None
    if weight is not None:
        bucket_name = f"{model}{POSTFIX_MODEL}"
        minio = Minio(endpoint, access_key, secret_key, secure=secure)
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
        except S3Error as e:
            print(e)


def add_model(args):
    endpoint, access_key, secret_key, secure = read_secret()
    model = args[0]
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
        merged = {**dict1, **dict2}
        with open(current_profile, 'w') as file:
            yaml.dump(merged, file)

        download_weight(args)
    except S3Error as e:
        print(e)


def remove_weight(args):
    weight = args[1] if len(args) > 1 else None
    if weight is not None:
        path = f"vsdkx/weight/{weight}"
        if os.path.exists(path):
            os.remove(path)


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

    remove_weight(args)


def install_addon(args):
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    install(f"vsdkx-addon-{args[0]}")


def uninstall_addon(args):
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    uninstall(f"vsdkx-addon-{args[0]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command",
                        choices=(
                            'model', 'weight', 'clean', 'config', 'addon'))
    parser.add_argument("subcommand", choices=('set', 'add', 'remove', ''),
                        default="", nargs="?")
    argcomplete.autocomplete(parser)
    args, unknown = parser.parse_known_args()
    if args.command == "model":
        if args.subcommand == "add" or args.subcommand == "set":
            add_model(unknown)
        if args.subcommand == "remove":
            remove_model(unknown)
    elif args.command == "weight":
        if args.subcommand == "add" or args.subcommand == "set":
            download_weight(unknown)
        if args.subcommand == "remove":
            remove_weight(unknown)
    elif args.command == "clean":
        clean_all()
    elif args.command == "config":
        config()
    elif args.command == "addon":
        if args.subcommand == "add" or args.subcommand == "set":
            install_addon(unknown)
        if args.subcommand == "remove":
            uninstall_addon(unknown)


if __name__ == "__main__":
    main()
