# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import dataclasses
import functools
import logging
import pathlib
import shutil
import subprocess
import tempfile

from .logger import LOGGER


@dataclasses.dataclass
class SavedFile:
    path: pathlib.Path
    remove_at_start: bool = False


@functools.total_ordering
class Version:
    def __init__(self, *args):
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


class ArtifactsCollector:
    def __init__(self, name, module=None, cls=None):
        self._path = self._init_path(name, module, cls)

    def _init_path(self, name, module, cls):
        p = pathlib.Path.cwd()
        p /= "artifacts"
        if module:
            p /= module.__name__
        if cls:
            p /= cls.__name__
        p /= name
        return p

    def copy(self, src):
        self._path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, self._path)


class NodeRunningData:
    def __init__(self, item):
        self._tempdir = tempfile.TemporaryDirectory()
        self.tmp_path = pathlib.Path(self._tempdir.name)
        self.artifacts = ArtifactsCollector(
            name=item.name,
            module=item.module,
            cls=item.cls,
        )
        self.logfile = self.tmp_path / "test.log"
        self.handler = logging.FileHandler(self.logfile, delay=True)
        self.handler.setFormatter(
            logging.Formatter(
                "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s"
            )
        )


def logged_run(*args, **kwargs):
    LOGGER.debug("running %s with options %s", list(*args), kwargs)
    check = kwargs.pop("check", False)
    proc = subprocess.run(*args, **kwargs)
    LOGGER.debug("result: %s", proc)
    if check:
        proc.check_returncode()
    return proc
