# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import pathlib
import subprocess

from .util import SavedFile


SUBMAN_FILES_TO_SAVE = (
    SavedFile(pathlib.Path("/etc/rhsm/rhsm.conf")),
    SavedFile(pathlib.Path("/var/log/rhsm/rhsm.log"), remove_at_start=True),
    SavedFile(pathlib.Path("/var/log/rhsm/rhsmcertd.log"), remove_at_start=True),
)


class SubscriptionManager:
    def __init__(self):
        pass

    @property
    def is_registered(self):
        proc = self.run("identity", check=False)
        if proc.returncode == 0:
            return True
        if proc.returncode == 1:
            return False
        proc.check_returncode()

    def run(self, *args, check=True):
        return subprocess.run(
            ["subscription-manager"] + list(args), check=check, capture_output=True
        )

    def config(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            if k.startswith(("server_", "rhsm_", "logging_")) and v is not None:
                args.append(f"--{k.replace('_', '.', 1)}={v}")
        if not args:
            return

        self.run("config", *args)

    def register(
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
            args.append("--org")
            args.append(org)
        if activationkey:
            args.append("--activationkey")
            args.append(activationkey)

        return self.run("register", *args, *extra_args)

    def unregister(self):
        return self.run("unregister")


def stop_rhsmcertd():
    subprocess.run(
        ["systemctl", "stop", "rhsmcertd.service"], check=True, capture_output=True
    )
    pkill_proc = subprocess.run(["pkill", "-e", "-x", "rhsmcertd"], capture_output=True)
    if pkill_proc.returncode not in [0, 1]:
        pkill_proc.check_returncode()
