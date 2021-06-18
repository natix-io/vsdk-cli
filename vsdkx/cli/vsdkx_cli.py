import argparse, argcomplete, os, shutil
import textwrap
from getpass import getpass
import re
import readline
from argparse import RawTextHelpFormatter
from minio import Minio, S3Error
import yaml
import subprocess
import sys

from vsdkx.core.util.io import get_env_dict

from vsdkx.cli.config import config_data

POSTFIX_MODEL = "-product"
NAME_REGEX = "^([A-Za-z0-9\-.:])+$"

manifest = {
    "vsdkx-model-yolo-torch": "git+https://gitlab+deploy-token-488362:aQbEo4kAqEhppoUe3Tyh@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-torch",
    "vsdkx-model-yolo-tflite": "git+https://gitlab+deploy-token-488360:bRkGozdPs1yUjjLQS4Zy@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-tflite",
    "vsdkx-model-yolo-facemask": "git+https://gitlab+deploy-token-488359:fhs2HLs2ZHLxSvPHbt84@gitlab.com/natix/cvison/vsdkx/vsdkx-model-yolo-mask",
    "vsdkx-model-bayesian": "git+https://gitlab+deploy-token-488354:wfv9ruzXiDj93Dw6wrmP@gitlab.com/natix/cvison/vsdkx/vsdkx-model-bayesian",
    "vsdkx-model-resnet": "git+https://gitlab+deploy-token-488358:QVhHopKVuY4MWMyCNDEa@gitlab.com/natix/cvison/vsdkx/vsdkx-model-resnet",
    "vsdkx-model-mobilenet": "git+https://gitlab+deploy-token-488355:bRf2y6xyhHjQZrUy_uzB@gitlab.com/natix/cvison/vsdkx/vsdkx-model-mobilenet",
    "vsdkx-addon-distant": "git+https://gitlab+deploy-token-488346:fjijyZBz2gStuv46anZs@gitlab.com/natix/cvison/vsdkx/vsdkx-addon-distant",
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
    if not os.path.exists(path):
        os.mkdir(path)


def delete_file(name):
    if os.path.exists(name):
        os.remove(name)


def clean_all():
    if os.path.exists("vsdkx"):
        shutil.rmtree("vsdkx", True)
    delete_file(".secret")
    delete_file("vsdkx-run.py")


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


def modify_app(name, remove=False):
    lines = [name]
    path = "vsdkx/.config"
    if os.path.exists(path):
        with open(path, "r") as file:
            for l in file:
                lines.append(l.strip())
    lines = sorted(set(lines))
    if remove:
        lines.remove(name)
    with open(path, "w") as file:
        for l in lines:
            file.write(l)
            file.write("\n")


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
        if dict2 is None:
            dict2 = {}
        merged = {**dict1, **dict2}
        with open(current_profile, 'w') as file:
            yaml.dump(merged, file)
        modify_app(f"model-{model}")
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
    modify_app(f"model-{model}", True)
    remove_weight(args)


def install_addon(args):
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    install(f"vsdkx-addon-{args[0]}")
    modify_app(f"addon-{args[0]}")


def uninstall_addon(args):
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    uninstall(f"vsdkx-addon-{args[0]}")
    modify_app(f"addon-{args[0]}", True)


def init_app():
    if not os.path.exists("vsdkx-run.py"):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(_ROOT, 'vsdkx-run.py')
        shutil.copyfile(path, "./vsdkx-run.py")
    reconfig()


def ask_for_config(first_key, second_key, name, settings):
    for k in config_data[name]:
        if k == "_class":
            continue
        if second_key is None:
            key = f"{first_key}.{k}"
        else:
            key = f"{first_key}.{second_key}.{k}"
        default_value = get_env_dict(settings, key,
                                     config_data[name][k])
        i = input(f"Asking for ({name}) {k} Enter to set "
                  f"{default_value}: ")
        if first_key not in settings:
            settings[first_key] = {}
        if second_key is None:
            settings[first_key][k] = \
                eval(i) if i else default_value
        else:
            if second_key not in settings[first_key]:
                settings[first_key][second_key] = {}
            settings[first_key][second_key][k] = \
                eval(i) if i else default_value

def app_config(name, settings):
    if name in config_data:
        if name.startswith("model-"):
            if "model" not in settings:
                settings["model"] = {}
            debug = input("Debug mode? empty to set False: ")
            settings["model"]["debug"] = True if debug else False
            settings["model"]["class"] = \
                config_data[name]["_class"]
            settings["model"]["profile"] = name[6:]
            ask_for_config("model", "settings", name, settings)

        elif name.startswith("addon-"):
            if "addons" not in settings:
                settings["addons"] = {}
            addon = name[6:]
            if addon not in settings["addons"]:
                settings["addons"][addon] = {}
            settings["addons"][addon]["class"] = \
                config_data[name]["_class"]
            ask_for_config("addons", addon, name, settings)

def reconfig(unknown):
    path = "vsdkx/.config"
    settings_path = "vsdkx/settings.yaml"
    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, "r") as file:
            settings = yaml.full_load(file)
    if os.path.exists(path):
        if len(unknown) == 0:
            with open(path) as file:
                for l in file:
                    name = l.strip()
                    if not name:
                        continue
                    app_config(name, settings)
        else:
            app_config(unknown[0], settings)
        with open(settings_path, "w") as file:
            yaml.dump(settings, file)


def config_drawing():
    settings_path = "vsdkx/settings.yaml"
    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, "r") as file:
            settings = yaml.full_load(file)
    ask_for_config("drawing", None, "drawing", settings)
    with open(settings_path, "w") as file:
        yaml.dump(settings, file)


def main():
    parser = argparse.ArgumentParser(usage="vsdx-cli [-h] {command} [{args}]",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("command",
                        choices=(
                            'model', 'weight', 'clean', 'config', 'addon',
                            'app'),
                        metavar="{command}",
                        help=textwrap.dedent(
                            """\
                            model: use model to add/remove vsdkx-models
                                example: 
                                    vsdkx-cli model add {model_name}
                                    vsdkx-cli model remove {model_name}
                            weight: use weight to add/remove particular weight for a particular model
                                example: 
                                    vsdkx-cli weight add {model_name} {weight_name}
                                    vsdkx-cli weight remove {model_name} {weight_name}
                                you can also use it this way: 
                                    vsdkx-cli model add {model_name} {weight_name}
                                    vsdkx-cli model remove {model_name} {weight_name}
                                    vsdkx-cli model set {model_name} {weight_name}
                            config: to set credentials and endpoint for the blob server you should first use this command
                                example:
                                    vsdkx-cli config
                            addon: to add any vsdkx-addon to your project you can use this command
                                example:
                                    vsdkx-cli addon add {addon_name}                                
                                    vsdkx-cli addon remove {addon_name}
                            clean: to clean all the added folders and files related to vsdkx you can use this command
                                example:
                                    vsdkx-cli clean
                            app: If you want to have vsdkx-run.py in your code which is a simple runner app then you should this command
                                example:
                                    vsdkx-cli app init
                            """))
    parser.add_argument("subcommand", choices=('set', 'add', 'remove', 'init',
                                               'config', 'draw', ''),
                        default="", nargs="?", metavar="{args}",
                        help=textwrap.dedent("""\
                        add: for model/weight/addon you can use this subcommand to add model/weight/addon
                        remove: for model/weight/addon you can use this subcommand to remove model/weight/addon
                        set: for model you can use this subcommand to set a particular weight for that model name
                        init: for app you can use this subcommand to init a simple runner file inside your project
                        config: for app you can use this subcommand to reconfigure the settings.yaml
                        draw: for app you can use this subcommand to reconfigure the settings.yaml for drawing
                        """))
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
    elif args.command == "app":
        if args.subcommand == "init":
            init_app()
        elif args.subcommand == "config":
            reconfig(unknown)
        elif args.subcommand == "draw":
            config_drawing()


if __name__ == "__main__":
    main()
