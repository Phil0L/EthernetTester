#!/usr/bin/env python

import subprocess
import os
import sys
from time import sleep
from update import status

VERSION = "0.1"
KW_RESTART = 'restart'
KW_NO_UPDATE_CHECK = 'no_update'
KW_DO_UPDATE = "update"
KW_UP_TO_DATE = 3


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")


def start():
    print("Started.")


def update_check():
    update_count = status()
    if update_count > 0:
        print(f"{update_count} updates available. Run 'python main.py update' to update")
    return update_count


def update():
    code = subprocess.call(["python", "update.py"], shell=False)
    if code == KW_UP_TO_DATE:
        return
    print("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv + [KW_RESTART, KW_NO_UPDATE_CHECK])
    exit(0)


if __name__ == "__main__":
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        update_check()
    start()
    sleep(5)

