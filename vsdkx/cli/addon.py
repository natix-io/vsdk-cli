from vsdkx.cli.global_constants import NAME_REGEX
from vsdkx.cli.util import install, modify_app, uninstall
import re, os, yaml


def install_addon(args):
    """
    Install addon to current project

    Args:
        args: args[0] should be the name of the addon
    """
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    install(f"vsdkx-addon-{args[0]}")
    modify_app(f"addon-{args[0]}")
    print(f"{args[0]} added")


def uninstall_addon(args):
    """
    Uninstall addon from current project

    Args:
        args: args[0] should be the name of the addon

    """
    assert re.match(NAME_REGEX, args[0]), \
        "addon name is not right"
    uninstall(f"vsdkx-addon-{args[0]}")
    modify_app(f"addon-{args[0]}", True)
    remove_addon_from_setting(args[0])
    print(f"{args[0]} removed")


def remove_addon_from_setting(name):
    """
    Removes config section for specific addon from vsdkx/settings.yaml

    Args:
        name: name of the addon
    """
    settings_path = "vsdkx/settings.yaml"
    if os.path.exists(settings_path):
        with open(settings_path, "r") as file:
            settings = yaml.full_load(file)
        if "addons" in settings:
            if name in settings["addons"]:
                settings["addons"].pop(name)
                with open(settings_path, "w") as file:
                    yaml.dump(settings, file)
