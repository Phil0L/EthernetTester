#!/usr/bin/env python

import subprocess


def main():
    update()


def update():
    print("Updating...")
    subprocess.call(["python", "update.py"])
    print("Updater called")


if __name__ == "__main__":
    main()
