#!/usr/bin/env python

import git  # pip install gitpython
from git import Repo


def pull():
    git_dir = "."
    g = git.cmd.Git(git_dir)
    msg = g.pull()
    print(msg)
    if msg == "Already up to date.":
        return 3
    print("Updating done.")
    return 4


def status():
    git_dir = "."
    repo = Repo(git_dir)
    repo.remotes.origin.fetch()
    local_branch = repo.active_branch
    local_branch_name = local_branch.name
    commits_behind = repo.iter_commits(f"{local_branch_name}..origin/main")
    count = sum(1 for _ in commits_behind)
    return count


if __name__ == '__main__':
    exit(pull())


