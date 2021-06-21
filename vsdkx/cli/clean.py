import os
import shutil

from vsdkx.cli.util import delete_file


def clean_all():
    """
    Removed all vsdkx stuff from current project
    """
    if os.path.exists("vsdkx"):
        shutil.rmtree("vsdkx", True)
    delete_file(".secret")
    delete_file("vsdkx-run.py")
