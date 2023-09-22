# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import json


class TestConfig:
    def __init__(self, test_config):
        self._test_config = self._load_config(test_config)
        self._is_external = test_config is not None

    @property
    def is_external(self):
        return self._is_external

    def _load_config(self, test_config):
        if not test_config:
            return {}
        with test_config.open("r") as f:
            return json.load(f)

    def get(self, *path):
        v = self._test_config
        for p in path:
            v = v[p]
        return v
