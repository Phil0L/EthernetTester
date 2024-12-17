#!/usr/bin/env python

import sys
from time import sleep

import display
from update import update_check, KW_DO_UPDATE, update, KW_NO_UPDATE_CHECK

VERSION = "0.2"


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")


def start():
    print("Started. Ctrl+C to quit.")
    display.initialize()


if __name__ == "__main__":
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        update_check()
    start()
    sleep(5)
