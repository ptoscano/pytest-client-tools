# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import time
import warnings

import requests

from .util import Version


class Candlepin:
    def __init__(self, host, port, prefix, insecure):
        self._running = False
        self._host = host
        self._port = port
        self._prefix = prefix
        self._insecure = insecure
        self._base_path = f"https://{self._host}:{self._port}{self._prefix}"
        self._session = requests.Session()
        self._request_kwargs = {
            "headers": {
                "Content-type": "application/json",
            },
            "verify": False,
        }

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def prefix(self):
        return self._prefix

    @property
    def insecure(self):
        return self._insecure

    def _request(self, req_type, path, **kwargs):
        actual_kwargs = self._request_kwargs
        actual_kwargs.update(kwargs)
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        response = self._session.request(
            req_type, f"{self._base_path}/{path}", **actual_kwargs
        )
        response.raise_for_status()
        return response

    def get(self, path, **kwargs):
        return self._request("GET", path)

    def status(self):
        return self.get("status").json()

    def version(self):
        return Version(self.status()["version"])


def ping_candlepin(candlepin, initial_wait=None):
    if initial_wait:
        time.sleep(initial_wait)
    for i in range(1, 60):
        try:
            candlepin.status()
            return
        except Exception as e:
            if i >= 59:
                raise e from None
            time.sleep(1)
