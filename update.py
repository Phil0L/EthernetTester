#!/usr/bin/env python
import os
import subprocess
import sys
import threading
from git import Repo, GitCommandError  # pip install gitpython
from data import Data

KW_RESTART = 'restart'
KW_NO_UPDATE_CHECK = 'no_update'
KW_DO_UPDATE = "update"
KW_UP_TO_DATE = 3
GITHUB_BRANCH = "origin/main"

executor_update: threading.Thread
update_count = 0


def status():
    try:
        return _status()
    except GitCommandError as e:
        print(e)
        return 0


def update():
    print("Launching Updater...")
    code = subprocess.call(["python", f"{os.getcwd()}/updater.py"] + sys.argv)
    print(code)
    if code == KW_UP_TO_DATE:
        return
    print("Restarting...")
    if KW_DO_UPDATE in sys.argv:
        sys.argv.remove(KW_DO_UPDATE)
    os.execv(sys.executable, ['python'] + sys.argv + [KW_RESTART, KW_NO_UPDATE_CHECK])
    exit(0)


def _status():
    git_dir = "."
    repo = Repo(git_dir)
    repo.remotes.origin.fetch()
    local_branch = repo.active_branch
    local_branch_name = local_branch.name
    commits_behind = repo.iter_commits(f"{local_branch_name}..{GITHUB_BRANCH}")
    count = sum(1 for _ in commits_behind)
    return count


def check_update(data: Data):
    global executor_update
    if executor_update is None or not executor_update.isAlive():
        executor_update = threading.Thread(target=_check_update())
        executor_update.start()
    data.update_count = update_count


def _check_update():
    global update_count
    update_count = status()
    print(f"DEBUG update_count = {update_count}")
