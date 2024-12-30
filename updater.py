#!/usr/bin/env python
import datetime
import sys
import git  # pip install gitpython

KW_LOGFILE = "logfile"


def pull():
    git_dir = "."
    g = git.cmd.Git(git_dir)
    msg = g.pull()
    print(msg)
    if msg == "Already up to date.":
        return 3
    print("Updating done.")
    return 4


if __name__ == '__main__':
    if KW_LOGFILE in sys.argv:
        sys.stdout = open('log.txt', 'a')
        sys.stderr = sys.stdout
        print(f"UPDATER STARTED AT {datetime.datetime.now().strftime('%I:%M  %B %d, %Y')}")
    exit(pull())
