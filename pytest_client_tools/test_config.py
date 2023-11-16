# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

from dynaconf import Dynaconf, Validator


class TestConfig:
    def __init__(self):
        self._settings = Dynaconf()
        self._settings.validators.register(
            Validator("candlepin.host"),
            Validator("candlepin.port", gt=0, lt=65536, cast=int, is_type_of=int),
            Validator("candlepin.prefix", startswith="/"),
            Validator("candlepin.insecure", cast=bool, is_type_of=bool),
            Validator("candlepin.username"),
            Validator(
                "candlepin.password",
                must_exist=True,
                when=Validator("candlepin.username", must_exist=True),
            ),
        )
        self._settings.validators.validate()

    @property
    def is_external(self):
        try:
            return (
                self._settings.get("candlepin.host") is not None
                and self._settings.get("candlepin.port") is not None
                and self._settings.get("candlepin.prefix") is not None
                and self._settings.get("candlepin.username") is not None
                and self._settings.get("candlepin.password") is not None
            )
        except KeyError:
            return False

    def get(self, *path):
        return self._settings[".".join(path)]
