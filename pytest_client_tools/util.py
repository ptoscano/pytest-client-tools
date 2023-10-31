# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import dataclasses
import functools
import pathlib
import shutil
import tempfile


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
