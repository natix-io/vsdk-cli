import argparse, argcomplete
import textwrap

from argparse import RawTextHelpFormatter

from vsdkx.cli.addon import install_addon, uninstall_addon
from vsdkx.cli.app import init_app, app_reconfig, list_app
from vsdkx.cli.clean import clean_all
from vsdkx.cli.credential import repo_config
from vsdkx.cli.draw import config_drawing
from vsdkx.cli.model import add_model, remove_model
from vsdkx.cli.weight import download_weight, remove_weight


def main():
    parser = argparse.ArgumentParser(usage="vsdx-cli [-h] {command} [{args}]",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("command",
                        choices=(
                            'model', 'weight', 'clean', 'repo', 'addon',
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
                            repo: to set credentials and endpoint for the blob server you should first use this command
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
                                               'config', 'draw', 'list', ''),
                        default="", nargs="?", metavar="{args}",
                        help=textwrap.dedent("""\
                        add: for model/weight/addon you can use this subcommand to add model/weight/addon
                        remove: for model/weight/addon you can use this subcommand to remove model/weight/addon
                        set: for model you can use this subcommand to set a particular weight for that model name
                        init: for app you can use this subcommand to init a simple runner file inside your project
                        config: for app you can use this subcommand to reconfigure the settings.yaml
                        draw: for app you can use this subcommand to reconfigure the settings.yaml for drawing
                        list: for app you can use this subcommand to see the list of models and addons
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
    elif args.command == "repo":
        repo_config()
    elif args.command == "addon":
        if args.subcommand == "add" or args.subcommand == "set":
            install_addon(unknown)
        if args.subcommand == "remove":
            uninstall_addon(unknown)
    elif args.command == "app":
        if args.subcommand == "init":
            init_app()
        elif args.subcommand == "config":
            app_reconfig(unknown)
        elif args.subcommand == "draw":
            config_drawing()
        elif args.subcommand == "list":
            list_app()


if __name__ == "__main__":
    main()
