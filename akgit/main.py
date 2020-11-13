#!/bin/python3

import sys
import subprocess
from git import Repo
from pathlib import Path
args = sys.argv

PROTECTED = ["oca", "shopinvader"]

def get_root_dir(path=None):
    if path is None:
        path = Path(".").resolve()
    if (path / '.git').exists():
        return path
    else:
        return get_root_dir(path.parent)

def get_repo():
    path = get_root_dir()
    return Repo(str(path))

def ensure_remote_akretion():
    repo = get_repo()
    for remote in repo.remotes:
        if remote.name == "ak":
            return
    origin = repo.remotes[0].url.split("/")[-2]
    akretion_url = repo.remotes[0].url.replace(origin, "akretion")
    repo.create_remote("ak", akretion_url)

def ensure_no_protected_push(remote_name):
    repo = get_repo()
    for remote in repo.remotes:
        if remote.name == remote_name:
            org = remote.url.lower().split("/")[-2]
            if org in PROTECTED:
                raise Exception("No direct push to %s" % org)

def check_push(args):
    if len(args) >= 3:
        org = args[2]
    else:
        org = "origin"
    if org == "ak":
        ensure_remote_akretion()
    else:
        ensure_no_protected_push(org)

def check_commit(args):
    path = get_root_dir()
    # install pre-commit if needed
    if (path / ".pre-commit-config.yaml").exists()\
            and not (path / ".git" / "hooks" / "pre-commit").exists():
        subprocess.run(["pre-commit", "install"])


def main():
    if args[1] == "clone":
        print("Auto-share")
        subprocess.run(["/usr/bin/git", "autoshare-clone"] + args[2:])
    else:
        if args[1] == "push":
            check_push(args)
        elif args[1] == "commit":
            check_commit(args)
        subprocess.run(["/usr/bin/git"] + args[1:])
