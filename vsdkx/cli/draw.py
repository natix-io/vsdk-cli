import os
import yaml

from vsdkx.cli.app import ask_for_config


def config_drawing():
    settings_path = "vsdkx/settings.yaml"
    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, "r") as file:
            settings = yaml.full_load(file)
    ask_for_config("drawing", None, "drawing", settings)
    with open(settings_path, "w") as file:
        yaml.dump(settings, file)
