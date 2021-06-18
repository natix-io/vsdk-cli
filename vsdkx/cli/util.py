import os
import subprocess
import sys

from vsdkx.core.util.io import get_env_dict
from vsdkx.cli.config import config_data
from vsdkx.cli.global_constants import manifest


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def delete_file(name):
    if os.path.exists(name):
        os.remove(name)


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


def modify_app(name: str, remove=False):
    lines = [name]
    path = "vsdkx/.config"
    if os.path.exists(path):
        with open(path, "r") as file:
            for l in file:
                if name.startswith("model-"):
                    if l.strip().startswith("model-"):
                        continue
                else:
                    lines.append(l.strip())
    lines = sorted(set(lines))
    if remove:
        lines.remove(name)
    with open(path, "w") as file:
        for l in lines:
            file.write(l)
            file.write("\n")


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
