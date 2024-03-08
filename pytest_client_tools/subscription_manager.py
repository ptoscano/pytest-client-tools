# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import pathlib
import subprocess

from .util import SavedFile, logged_run


SUBMAN_FILES_TO_SAVE = (
    SavedFile(pathlib.Path("/etc/rhsm/rhsm.conf")),
    SavedFile(pathlib.Path("/var/log/rhsm/rhsm.log"), remove_at_start=True),
    SavedFile(pathlib.Path("/var/log/rhsm/rhsmcertd.log"), remove_at_start=True),
)


class SubscriptionManager:
    """
    Subscription Manager.

    This class represents the `subscription-manager` tool.
    """

    def __init__(self):
        pass

    @property
    def is_registered(self):
        """
        Query whether `subscription-manager` is registered.

        :return: Whether `subscription-manager` is registered
        :rtype: bool
        """
        proc = self.run("identity", check=False)
        if proc.returncode == 0:
            return True
        if proc.returncode == 1:
            return False
        proc.check_returncode()

    def run(self, *args, check=True, text=True):
        """
        Run `subscription-manager` with the specified arguments.

        This function is a simple wrapper around invoking
        `subscription-manager` with a specified list of arguments, returning
        the result of the execution directly from `subprocess`.

        :return: The result of the command execution
        :rtype: `subprocess.CompletedProcess`
        """
        return logged_run(
            ["subscription-manager"] + list(args),
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text,
        )

    def config(self, **kwargs):
        args = []
        sections = ("server_", "rhsm_", "rhsmcertd_", "logging_")
        for k, v in kwargs.items():
            if k.startswith(sections) and v is not None:
                args.append(f"--{k.replace('_', '.', 1)}={v}")
        if not args:
            return

        self.run("config", *args)

    def register(
        self,
        username=None,
        password=None,
        org=None,
        activationkey=None,
        environments=None,
        *extra_args,
    ):
        """
        Register with `subscription-manager`.

        Invokes `subscription-manager register`.

        :return: The result of the command execution
        :rtype: `subprocess.CompletedProcess`
        """
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
            if isinstance(activationkey, list):
                args.append(",".join(activationkey))
            else:
                args.append(activationkey)
        if environments:
            args.append("--environment")
            if isinstance(environments, list):
                args.append(",".join(environments))
            else:
                args.append(environments)

        return self.run("register", *args, *extra_args)

    def unregister(self):
        """
        Unregister with `subscription-manager`.

        Invokes `subscription-manager unregister`.

        :return: The result of the command execution
        :rtype: `subprocess.CompletedProcess`
        """
        return self.run("unregister")


def stop_rhsmcertd():
    logged_run(
        ["systemctl", "stop", "rhsmcertd.service"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    pkill_proc = logged_run(
        ["pkill", "-e", "-x", "rhsmcertd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if pkill_proc.returncode not in [0, 1]:
        pkill_proc.check_returncode()
