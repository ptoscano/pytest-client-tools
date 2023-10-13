# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import pathlib
import subprocess

from .util import SavedFile


INSIGHTS_CLIENT_FILES_TO_SAVE = (
    SavedFile(pathlib.Path("/etc/insights-client/insights-client.conf")),
    SavedFile(
        pathlib.Path("/var/log/insights-client/insights-client.log"),
        remove_at_start=True,
    ),
    SavedFile(
        pathlib.Path("/var/log/insights-client/insights-client.log.1"),
        remove_at_start=True,
    ),
    SavedFile(
        pathlib.Path("/var/log/insights-client/insights-client.log.2"),
        remove_at_start=True,
    ),
    SavedFile(
        pathlib.Path("/var/log/insights-client/insights-client.log.3"),
        remove_at_start=True,
    ),
)


class InsightsClient:
    def __init__(self):
        pass

    @property
    def is_registered(self):
        proc = self.run("--status", check=False)
        print(proc)
        if proc.returncode in [0, 1] and any(
            i in proc.stdout for i in [b"NOT", b"unregistered"]
        ):
            return False
        if proc.returncode == 0 and any(
            i in proc.stdout for i in [b"This host is registered", b"Registered"]
        ):
            return True
        proc.check_returncode()

    def run(self, *args, check=True):
        return subprocess.run(
            ["insights-client"] + list(args), check=check, capture_output=True
        )

    def register(self):
        return self.run("--register")

    def unregister(self):
        return self.run("--unregister")
