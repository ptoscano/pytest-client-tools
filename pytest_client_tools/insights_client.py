# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import configparser
import pathlib
import subprocess

from .util import SavedFile, logged_run


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


class InsightsClientConfig:
    # boolean config keys
    _KEYS_BOOL = {
        "analyze_container",
        "analyze_image_idanalyze_file",
        "analyze_mountpoint",
        "auto_config",
        "auto_update",
        "build_packagecache",
        "check_results",
        "checkin",
        "compliance",
        "core_collect",
        "debug",
        "disable_schedule",
        "enable_schedule",
        "force",
        "gpg",
        "keep_archive",
        "legacy_upload",
        "list_specs",
        "net_debug",
        "no_gpg",
        "no_upload",
        "obfuscate",
        "obfuscate_hostname",
        "offline",
        "quiet",
        "register",
        "reregister",
        "show_results",
        "silent",
        "status",
        "support",
        "test_connection",
        "to_json",
        "unregister",
    }
    # int config keys
    _KEYS_INT = {
        "retries",
        "cmd_timeout",
    }
    # float config keys
    _KEYS_FLOAT = {
        "http_timeout",
    }

    def __init__(self, path="/etc/insights-client/insights-client.conf"):
        self._path = path
        self.reload()

    def reload(self):
        with open(self._path) as f:
            self._config = configparser.ConfigParser()
            self._config.read_file(f, source=self._path)

    def __getattr__(self, name):
        if name in self._KEYS_BOOL:
            read_func = self._config.getboolean
        elif name in self._KEYS_INT:
            read_func = self._config.getint
        elif name in self._KEYS_FLOAT:
            read_func = self._config.getfloat
        else:
            read_func = self._config.get
        try:
            return read_func("insights-client", name)
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise KeyError(name)


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
        return logged_run(
            ["insights-client"] + list(args),
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def register(self):
        return self.run("--register")

    def unregister(self):
        return self.run("--unregister")
