#!/usr/bin/env python

import subprocess


def main():
    update()


def update():
    print("Updating...")
    subprocess.call(["python", "update.py"])


if __name__ == "__main__":
    main()
