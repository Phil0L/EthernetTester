#!/usr/bin/env python

import subprocess
import os
import sys

VERSION = "0.01"


def main():
    print("Ethernet tester successfully started.")
    print(f"Version: {VERSION}")
    update()


def update():
    print("Updating...")
    subprocess.call(["python", "update.py"], shell=True)
    print("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == "__main__":
    main()
