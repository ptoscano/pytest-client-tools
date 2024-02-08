# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT


import pytest

from pytest_client_tools.insights_client import InsightsClientConfig


def test_config_not_existing(tmp_path):
    with pytest.raises(FileNotFoundError):
        InsightsClientConfig(str(tmp_path / "not-existing.conf"))


def test_config_missing_main_section(tmp_path):
    conf_file = tmp_path / "file.conf"
    conf_file.write_text(
        """[foo]
authmethod=CERT
"""
    )
    conf = InsightsClientConfig(conf_file)
    with pytest.raises(KeyError):
        assert conf.authmethod == "CERT"


def test_config_missing_key(tmp_path):
    conf_file = tmp_path / "file.conf"
    conf_file.write_text(
        """[insights-client]
auto_config=True
"""
    )
    conf = InsightsClientConfig(conf_file)
    with pytest.raises(KeyError):
        assert conf.authmethod == "CERT"


def test_config_existing_keys(tmp_path):
    conf_file = tmp_path / "file.conf"
    conf_file.write_text(
        """[insights-client]
auto_config=True
authmethod=CERT
cmd_timeout=120
http_timeout=120
        """
    )
    conf = InsightsClientConfig(conf_file)
    # bool
    assert conf.auto_config
    assert isinstance(conf.auto_config, bool)
    # string
    assert conf.authmethod == "CERT"
    assert isinstance(conf.authmethod, str)
    # int
    assert conf.cmd_timeout == 120
    assert isinstance(conf.cmd_timeout, int)
    # float
    assert conf.http_timeout == 120
    assert isinstance(conf.http_timeout, float)


def test_config_reload(tmp_path):
    conf_file = tmp_path / "file.conf"
    conf_file.write_text(
        """[insights-client]
auto_config=True
"""
    )
    conf = InsightsClientConfig(conf_file)
    assert conf.auto_config
    conf_file.write_text(
        """[insights-client]
auto_config=False
"""
    )
    conf.reload()
    assert not conf.auto_config
