# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT


import pytest

from pytest_client_tools.util import Version


@pytest.mark.parametrize(
    "input_string,expected_string",
    [
        ("1", "1"),
        ("1.2", "1.2"),
        ("1.0", "1.0"),
        ("5.1.8", "5.1.8"),
        ("5.1.10.25", "5.1.10.25"),
    ],
)
def test_version_from_string(input_string, expected_string):
    assert str(Version(input_string)) == expected_string


@pytest.mark.parametrize(
    "input_values,expected_string",
    [
        ([1], "1"),
        ([1, 2], "1.2"),
        ([1, 0], "1.0"),
        ([5, 1, 8], "5.1.8"),
        ([5, 1, 10, 25], "5.1.10.25"),
    ],
)
def test_version_from_values(input_values, expected_string):
    assert str(Version(*input_values)) == expected_string
