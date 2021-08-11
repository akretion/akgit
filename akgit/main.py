#!/bin/python3

import sys
import subprocess
from git import Repo
from pathlib import Path
args = sys.argv

PROTECTED = ["oca", "shopinvader"]

REMOTE_ALIAS = {
    "ak": "akretion",
    "c2c": "camptocamp",
    "acs": "acsone",
    }

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

def ensure_remote(remote_name):
    repo = get_repo()
    for remote in repo.remotes:
        if remote.name == remote_name:
            return
    remote_split_url = repo.remotes[0].url.split("/")
    remote_split_url[-2] = REMOTE_ALIAS.get(remote_name, remote_name)
    remote_url = "/".join(remote_split_url)
    repo.create_remote(remote_name, remote_url)

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
    ensure_no_protected_push(org)
    ensure_remote(org)

def check_commit(args):
    path = get_root_dir()
    # install pre-commit if needed
    if (path / ".pre-commit-config.yaml").exists()\
            and not (path / ".git" / "hooks" / "pre-commit").exists():
        subprocess.run(["pre-commit", "install"])

def check_fetch(args):
    if len(args) > 2:
        ensure_remote(args[2])


def main():
    if args[1] == "clone":
        print("Auto-share")
        subprocess.run(["/usr/bin/git", "autoshare-clone"] + args[2:])
    else:
        if args[1] == "push":
            check_push(args)
        elif args[1] == "commit":
            check_commit(args)
        elif args[1] == "fetch":
            check_fetch(args)
        subprocess.run(["/usr/bin/git"] + args[1:])
