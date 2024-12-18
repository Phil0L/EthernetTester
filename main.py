#!/usr/bin/env python
import os
import datetime
import sys
import display
import touch
from data import Data
from update import update_check, KW_DO_UPDATE, update, KW_NO_UPDATE_CHECK

VERSION = "0.2.4"
KW_LOGFILE = "logfile"
data = Data()


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")


def update_clicked():
    update_check()


def console_clicked():
    pass


def start():
    print("Started. Ctrl+C to quit.")
    data.version = VERSION
    display.initialize()
    display.on_update_clicked(lambda _: update_clicked())
    display.on_console_clicked(lambda _: console_clicked())
    touch.initialize()


def loop():
    display.draw(data)
    touch.check_touch(data.touch)


if __name__ == "__main__":
    if KW_LOGFILE in sys.argv:
        print(f"APPLICATION STARTED AT {datetime.datetime.now().strftime('%I:%M  %B %d, %Y')}")
        sys.stdout = open('log.txt', 'w')
        sys.stderr = sys.stdout
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        update_count = update_check()
    start()
    while True:
        loop()
