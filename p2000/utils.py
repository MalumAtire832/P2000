import json
import os
import subprocess
# "Program 'rtl-fm' not installed, see the Setup section in the README for more info."

DEVNULL = open(os.devnull, 'w')


def load_config():
    """
    Load the config file as JSON.
    :return: The config file as JSON.
    """
    with open('./resources/config.json') as f:
        return json.load(f)


def is_rtlfm_installed():
    try:
        subprocess.call(["rtl_fm", "-h"], stdout=DEVNULL, stderr=subprocess.STDOUT, close_fds=True)
        return True
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
        else:
            raise


def is_multimon_installed():
    try:
        subprocess.call(["rtl_fm", "-h"], stdout=DEVNULL, stderr=subprocess.STDOUT, close_fds=True)
        return True
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
        else:
            raise
