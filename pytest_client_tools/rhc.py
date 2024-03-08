# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import json
import pathlib
import subprocess

from .util import SavedFile, logged_run


RHC_FILES_TO_SAVE = (
    SavedFile(pathlib.Path("/etc/rhc/config.toml")),
    SavedFile(pathlib.Path("/etc/rhc/workers/rhc-package-manager.toml")),
)


class Rhc:
    """
    Rhc.

    This class represents the `rhc` tool.
    """

    def __init__(self):
        pass

    @property
    def is_registered(self):
        """
        Query whether `rhc` is registered.

        :return: Whether `rhc` is registered
        :rtype: bool
        """
        proc = self.run("status", "--format", "json")
        doc = json.loads(proc.stdout)
        return doc["rhsm_connected"]

    def run(self, *args, check=True, text=True):
        """
        Run `rhc` with the specified arguments.

        This function is a simple wrapper around invoking `rhc` with a
        specified list of arguments, returning the result of the execution
        directly from `rhc`.

        :return: The result of the command execution
        :rtype: `subprocess.CompletedProcess`
        """
        return logged_run(
            ["rhc"] + list(args),
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text,
        )

    def connect(
        self, username=None, password=None, org=None, activationkey=None, *extra_args
    ):
        """
        Connect with `rhc`.

        Invokes `rhc connect`.

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
        """
        Disconnect with `rhc`.

        Invokes `rhc disconnect`.

        :return: The result of the command execution
        :rtype: `subprocess.CompletedProcess`
        """
        return self.run("disconnect")
