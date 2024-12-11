#!/usr/bin/env python

import subprocess
import os
import sys
from time import sleep
from update import status

VERSION = "0.03"
KW_RESTART = 'restart'
KW_NO_UPDATE_CHECK = 'no_update'
KW_DO_UPDATE = "update"
KW_UP_TO_DATE = 3


def main():
    print("Ethernet tester successfully started.")
    print(f"Version: {VERSION}")


def update_check():
    print("Checking for updates...")
    update_count = status()
    if update_count == 0:
        print("Already up to date.")
    else:
        print(f"{update_count} updates available.")
    return update_count


def update():
    code = subprocess.call(["python", "update.py"], shell=False)
    if code == KW_UP_TO_DATE:
        return
    print("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv + [KW_RESTART, KW_NO_UPDATE_CHECK])
    exit(0)


if __name__ == "__main__":
    if KW_NO_UPDATE_CHECK not in sys.argv:
        update_check()
    if KW_DO_UPDATE in sys.argv:
        update()
    main()
    sleep(5)

