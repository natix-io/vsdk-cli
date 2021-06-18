import os
import shutil
import yaml
from vsdkx.cli.config import config_data
from vsdkx.cli.util import ask_for_config


def init_app():
    if not os.path.exists("vsdkx-run.py"):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(_ROOT, 'vsdkx-run.py')
        shutil.copyfile(path, "./vsdkx-run.py")
    app_reconfig([])


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


def app_reconfig(unknown):
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


def list_app():
    path = "vsdkx/.config"
    if os.path.exists(path):
        lines = []
        with open(path, "r") as file:
            for l in file:
                lines.append(l.strip())
        lines = sorted(set(lines))
        for line in lines:
            print(line)
