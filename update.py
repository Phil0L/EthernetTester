#!/usr/bin/env python

import git  # pip install gitpython


def pull():
    git_dir = "."
    g = git.cmd.Git(git_dir)
    msg = g.pull()
    print(msg)


if __name__ == '__main__':
    pull()
