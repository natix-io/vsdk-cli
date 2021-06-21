import os
import subprocess
import sys

from vsdkx.core.util.io import get_env_dict
from vsdkx.cli.config import config_data
from vsdkx.cli.global_constants import manifest


def create_folder(path):
    """
    Create a folder for the path if it doesn't exist

    Args:
        path: the path to folder
    """
    if not os.path.exists(path):
        os.mkdir(path)


def delete_file(name):
    """
    if name exists then it would remove the file

    Args:
        name: the name of the file
    """
    if os.path.exists(name):
        os.remove(name)


def install(package):
    """
    Install pip package for current python environment

    Args:
        package: the name of the package
    """
    if manifest.get(package) is not None:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               manifest[package]])
        modify_requirement(package)
    else:
        print(f"No package {package} found")


def uninstall(package):
    """
    Uninstall pip package for current python environment

    Args:
        package: the name of the package
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall",
                               package])
        modify_requirement(package, True)
    except:
        pass


def modify_requirement(package, remove=False):
    """
    Add/Remove package names in requirements.txt file for current project

    Args:
        package: the name of the package
        remove: True if we want to remove it from requirements.txt else False
    """
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
    """
    Add/Remove model driver or addon in current project

    Args:
        name: the name of the model driver or addon, if it is addon it starts
        with addon- if it is model drivers name starts with model-
        remove: True if we want to remove model or addon else False
    """
    lines = [name]
    path = "vsdkx/.config"
    if os.path.exists(path):
        with open(path, "r") as file:
            for l in file:
                if not remove and name.startswith("model-"):
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
    """
    Internal function to ask question for every parameter for each model driver
    or addon or drawing section in vsdkx/settings.yaml

    Args:
        first_key: the top level key section of settings.yaml
        second_key: the second level key section of settings.yaml
        name: the name of the model or addon in config_data
        settings: dictionary data of settings.yaml
    """
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
