# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import pytest
from dynaconf import Dynaconf, Validator

#
# it is necessary to use define global variable since dynaconf settings object
# is used even in pytest hooks to get config properties
#
_settings = Dynaconf(
    envvar_prefix="PYTEST_CLIENT_TOOLS",
    settings_files=["settings.toml", ".secrets.toml"],
)


@pytest.fixture
def settings(scope="session"):
    _settings.validators.register(
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
    _settings.validators.validate()
    return _settings
