#!/bin/python3


import sys
import subprocess

# Force git path before calling importing git
import os
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "/usr/bin/git"

from git import Repo
from pathlib import Path
args = sys.argv

PROTECTED = ["oca", "shopinvader"]

REMOTE_ALIAS = {
    "ak": "akretion",
    "c2c": "camptocamp",
    "acs": "acsone",
    }

AUTO_ADD_REMOTE = [
    "akretion",
    "camptocamp",
    "acsone",
    "oca",
    ]

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
    if remote_name in AUTO_ADD_REMOTE:
        repo.create_remote(remote_name, remote_url)

def ensure_no_protected_push(remote_name):
    repo = get_repo()
    for remote in repo.remotes:
        if remote.name == remote_name:
            org = remote.url.lower().split("/")[-2]
            if org in PROTECTED:
                raise Exception("No direct push to %s" % org)

def check_push(args):
    if len(args) >= 3 and args[2][0:2] != '--':
        org = args[2]
    elif len(args) == 2:
        org = "origin"
    else:
        # complex push cmd we do nothing, just use git
        return
    ensure_no_protected_push(org)
    ensure_remote(org)

def check_commit(args):
    path = get_root_dir()
    # install pre-commit if needed
    if (path / ".pre-commit-config.yaml").exists()\
            and not (path / ".git" / "hooks" / "pre-commit").exists():
        subprocess.run(["pre-commit", "install"])

def check_fetch(args):
    if len(args) == 3:
        ensure_remote(args[2])


def main():
    cmd = args[0].split("/")[-1]
    if cmd in ["sgit", "supergit"]:
        print("Call native git without hack")
        os.execv("/usr/bin/git", ['/usr/bin/git'] + args[1:])
    if args[1] == "clone":
        print("Autoshare")
        subprocess.run(["/usr/bin/git", "autoshare-clone"] + args[2:], check=True)
    else:
        if args[1] == "push":
            for key in ["-f", "--force"]:
                if key in args:
                    idx = args.index(key)
                    print("Replace --force by --force-with-lease")
                    args[idx] = "--force-with-lease"
            check_push(args)
        elif args[1] == "commit":
            check_commit(args)
        elif args[1] == "fetch":
            check_fetch(args)
        os.execv("/usr/bin/git", ['/usr/bin/git'] + args[1:])
