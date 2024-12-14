#!/usr/bin/env python

import git  # pip install gitpython


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
    exit(pull())
