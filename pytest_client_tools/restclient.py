# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import requests
import urllib3


class RestClient:
    """
    RestClient

    This class represents a client to perform REST calls.
    """

    def __init__(self, base_url, verify=True, cert=None):
        self._base_url = base_url
        self._verify = verify
        self._session = requests.Session()
        self._request_kwargs = {
            "headers": {
                "Content-type": "application/json",
            },
            "verify": self._verify,
        }
        if cert:
            self._request_kwargs["cert"] = cert

    @property
    def base_url(self):
        """
        The base URL of the REST server.
        """
        return self._base_url

    def _request(self, req_type, path, **kwargs):
        actual_kwargs = self._request_kwargs
        actual_kwargs.update(kwargs)
        if not self._verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = self._session.request(
            req_type, f"{self._base_url}/{path}", **actual_kwargs
        )
        response.raise_for_status()
        return response

    def get(self, path, **kwargs):
        """
        Perform a GET REST call.
        """
        return self._request("GET", path, **kwargs)
