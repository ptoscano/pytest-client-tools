# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import json
import pathlib

from .util import SavedFile, logged_run


RHC_FILES_TO_SAVE = (
    SavedFile(pathlib.Path("/etc/rhc/config.toml")),
    SavedFile(pathlib.Path("/etc/rhc/workers/rhc-package-manager.toml")),
)


class Rhc:
    def __init__(self):
        pass

    @property
    def is_registered(self):
        proc = self.run("status", "--format", "json")
        doc = json.loads(proc.stdout.decode())
        return doc["rhsm_connected"]

    def run(self, *args, check=True):
        return logged_run(["rhc"] + list(args), check=check, capture_output=True)

    def connect(
        self, username=None, password=None, org=None, activationkey=None, *extra_args
    ):
        args = []
        if username:
            args.append("--username")
            args.append(username)
        if password:
            args.append("--password")
            args.append(password)
        if org:
            args.append("--organization")
            args.append(org)
        if activationkey:
            args.append("--activation-key")
            args.append(activationkey)

        proc = self.run("connect", *args, *extra_args, check=False)
        if proc.returncode not in [0, 1]:
            proc.check_returncode()
        return proc

    def disconnect(self):
        return self.run("disconnect")
