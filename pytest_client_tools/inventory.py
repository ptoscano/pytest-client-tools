# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

from .restclient import RestClient


class Inventory:
    """
    Inventory

    This class represents an Inventory server.
    """

    def __init__(self, base_url, verify=True):
        self._rest_client = RestClient(
            base_url=base_url,
            verify=verify,
            cert=(
                "/etc/pki/consumer/cert.pem",
                "/etc/pki/consumer/key.pem",
            ),
        )
        self._insights_client = None

    @property
    def base_url(self):
        """
        The base URL of the Inventory server.
        """
        return self._rest_client.base_url

    def get(self, path, **kwargs):
        """
        Perform a GET REST call.
        """
        return self._rest_client.get(path, **kwargs)

    def this_system(self):
        """
        Query Inventory for the current system.

        This assumes the current system is already registered with
        `insights-client`. Raises `SystemNotRegisteredError` if the system
        is not registered.

        :return: The dict of the current system in Inventory
        :rtype: dict
        """
        if not self._insights_client:
            raise RuntimeError(
                "Inventory.this_system(): cannot invoke without insights_client"
            )
        path = f"hosts?insights_id={self._insights_client.uuid}"
        res_json = self.get(path).json()
        if res_json["total"] != 1:
            raise RuntimeError(
                f"Inventory.this_system(): {res_json['total']} hosts returned "
                f"for the current UUID ({self._insights_client.uuid})"
            )
        return res_json["results"][0]
