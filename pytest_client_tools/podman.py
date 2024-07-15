# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import contextlib
import functools
import subprocess


class ContainerNotRunningError(RuntimeError):
    """
    The container is not running.
    """

    def __init__(self):
        pass


def requires_running(func):
    @functools.wraps(func)
    def function_wrapper(self, *args, **kwargs):
        running_id = getattr(self, "_running_id")
        if not running_id:
            raise ContainerNotRunningError
        return func(self, *args, **kwargs)

    return function_wrapper


class Podman:
    def __init__(
        self,
        image,
        name=None,
        hostname=None,
        port_mappings=None,
    ):
        self._running_id = None
        self._image = image
        self._name = name
        self._hostname = hostname
        self._port_mappings = port_mappings

    @property
    def running_id(self):
        return self._running_id

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, error_type, error_value, traceback):
        with contextlib.suppress(ContainerNotRunningError):
            self.stop()
        if error_type:
            raise

    def run(self):
        if self._running_id:
            return

        args = [
            "podman",
            "run",
            "-d",
            "--pull=newer",
            "--rm",
        ]
        if self._name:
            args.append("--name")
            args.append(self._name)
        if self._hostname:
            args.append("--hostname")
            args.append(self._hostname)
        for port_mapping in self._port_mappings:
            args.append("-p")
            args.append(":".join([str(p) for p in port_mapping]))
        args.append(self._image)

        proc = subprocess.run(
            args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self._running_id = proc.stdout.rstrip().decode()

    @requires_running
    def stop(self):
        subprocess.run(
            ["podman", "stop", self._running_id],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._running_id = None
