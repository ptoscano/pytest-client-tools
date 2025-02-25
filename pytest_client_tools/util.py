# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import dataclasses
import functools
import logging
import pathlib
import shutil
import subprocess
import sys
import tempfile

from .logger import LOGGER


@dataclasses.dataclass
class SavedFile:
    path: pathlib.Path
    remove_at_start: bool = False


@functools.total_ordering
class Version:
    """
    Version.

    A simple representation of a version number/string in the format `X`,
    or `X.Y`, or `X.Y.Z`, or in general a sequence of dot-spearated numbers.
    Pre-release markers such as "alpha/beta/etc" are not supported.
    """

    def __init__(self, *args):
        """
        Create a new Version object.

        The passed arguments can either of:

        - a single string which is parsed
        - integer arguments representing the component of the version number

        Examples:
        ```python
        >>> Version("1.2")
        Version(1.2)
        >>> Version(1, 3)
        Version(1.3)
        >>> Version(1, 3) == Version("1.2")
        False
        >>> Version(1, 3, 1) >= Version("1.3")
        True
        ```
        """
        if len(args) == 1 and isinstance(args[0], str):
            parts = args[0].split(".")
            self._bits = [int(p) for p in parts]
        else:
            self._bits = [int(p) for p in args]

    def __lt__(self, other):
        if not isinstance(other, Version):
            return False
        return self._bits < other._bits

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return self._bits == other._bits

    def __str__(self):
        return ".".join([str(i) for i in self._bits])

    def __repr__(self):
        return f"Version({self.__str__()})"


class ClientToolsPluginData:
    def __init__(self):
        self.running_data = {}


class ArtifactsCollector:
    def __init__(self, name=None, module=None, cls=None):
        self._path = self._init_path(name, module, cls)

    def _init_path(self, name, module, cls):
        p = pathlib.Path.cwd()
        p /= "artifacts"
        if module:
            p /= module.__name__
        if cls:
            p /= cls.__name__
        if name:
            p /= name
        return p

    def copy(self, src):
        self._path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, self._path)

    def write_text(self, fn, data):
        (self._path / fn).write_text(data)


class NodeRunningData:
    def __init__(self, item=None):
        self._tempdir = tempfile.TemporaryDirectory()
        self.tmp_path = pathlib.Path(self._tempdir.name)
        self.artifacts = ArtifactsCollector(
            name=item.name if item else None,
            module=item.module if item else None,
            cls=item.cls if item else None,
        )
        self.logfile = self.tmp_path / "test.log"
        self.handler = logging.FileHandler(self.logfile, delay=True)
        self.handler.setFormatter(
            logging.Formatter(
                "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s"
            )
        )


def logged_run(*args, **kwargs):
    LOGGER.debug("running %s with options %s", args, kwargs)
    check = kwargs.pop("check", False)
    # switch "text" (if present) into "universal_newlines" for Python < 3.7
    if sys.version_info[:2] < (3, 7):
        text = kwargs.pop("text", None)
        if text is not None:
            kwargs["universal_newlines"] = text
    proc = subprocess.run(*args, **kwargs)
    LOGGER.debug("result: %s", proc)
    if check:
        proc.check_returncode()
    return proc
