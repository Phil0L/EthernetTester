#!/usr/bin/env python
import os
import subprocess
import sys
import threading
from time import sleep
from git import Repo, GitCommandError  # pip install gitpython

KW_RESTART = 'restart'
KW_NO_UPDATE_CHECK = 'no_update'
KW_DO_UPDATE = "update"
KW_UP_TO_DATE = 3
GITHUB_BRANCH = "origin/main"

stop_signal = False


def update_check():
    try:
        update_count = status()
        # DEBUG
        print(f"update_count = {update_count}")
        if update_count > 0:
            print(f"{update_count} updates available. Run 'python main.py update' to update")
        return update_count
    except GitCommandError as e:
        print(e)
        return 0


def update():
    global stop_signal
    stop_signal = True
    code = subprocess.call(["python", "updater.py"], shell=False)
    if code == KW_UP_TO_DATE:
        return
    print("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv + [KW_RESTART, KW_NO_UPDATE_CHECK])
    exit(0)


def status():
    git_dir = "."
    repo = Repo(git_dir)
    repo.remotes.origin.fetch()
    local_branch = repo.active_branch
    local_branch_name = local_branch.name
    commits_behind = repo.iter_commits(f"{local_branch_name}..{GITHUB_BRANCH}")
    count = sum(1 for _ in commits_behind)
    return count


def start_update_loop(callback):
    thread = threading.Thread(target=_update_loop, args=(callback,))
    thread.start()


def _update_loop(callback):
    while not stop_signal:
        update_count = update_check()
        callback(update_count)
        sleep(10)

