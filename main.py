#!/usr/bin/env python
import os
import datetime
import sys
import display
import touch
import update
from data import Data
from update import KW_DO_UPDATE, KW_NO_UPDATE_CHECK

VERSION = "0.2.7"
KW_LOGFILE = "logfile"
data = Data()


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")


def update_clicked():
    update.update()


def console_clicked():
    pass


def updates_counted(update_count):
    data.update_count = update_count


def start():
    print("Started. Ctrl+C to quit.")
    data.version = VERSION
    display.initialize()
    display.on_update_clicked(lambda _: update_clicked())
    display.on_console_clicked(lambda _: console_clicked())
    touch.initialize()
    update.start_update_loop(lambda update_count: updates_counted(update_count))
    touch.start_touch_loop(data.touch_data)


def loop():
    data.frame_count += 1
    display.draw(data)


if __name__ == "__main__":
    if KW_LOGFILE in sys.argv:
        sys.stdout = open('log.txt', 'w')
        sys.stderr = sys.stdout
        print(f"APPLICATION STARTED AT {datetime.datetime.now().strftime('%I:%M  %B %d, %Y')}")
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update.update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        data.update_count = update.update_check()
        if data.update_count > 0:
            print(f"{data.update_count} updates available. Run 'python main.py update' to update")
    start()
    while True:
        loop()
