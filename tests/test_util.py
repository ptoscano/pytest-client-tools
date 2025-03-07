# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT


import pytest

from pytest_client_tools.util import redact_arguments


@pytest.mark.parametrize(
    "args,redact_list,expected_args",
    [
        ([], [], []),
        (["a"], [], ["a"]),
        (["a", "--foo", "foo"], [], ["a", "--foo", "foo"]),
        (["a", "--foo=foo"], [], ["a", "--foo=foo"]),
        (["a", "--foo"], ["--foo"], ["a", "--foo"]),
        (["a", "--foo", "foo"], ["--foo"], ["a", "--foo", "<redacted>"]),
        (["a", "--foo", "foo"], ["--bar"], ["a", "--foo", "foo"]),
        (["a", "--foo=foo"], ["--foo"], ["a", "--foo=<redacted>"]),
        (["a", "--foo=foo"], ["--bar"], ["a", "--foo=foo"]),
        (["a", "--foo", "foo"], ["--unused", "--foo"], ["a", "--foo", "<redacted>"]),
        (["a", "--foo", "foo"], ["--unused", "--bar"], ["a", "--foo", "foo"]),
        (["a", "--foo=foo"], ["--unused", "--foo"], ["a", "--foo=<redacted>"]),
        (["a", "--foo=foo"], ["--unused", "--bar"], ["a", "--foo=foo"]),
        (["a", "--foobar", "foo"], ["--foo"], ["a", "--foobar", "foo"]),
        (["a", "--foobar=foo"], ["--foo"], ["a", "--foobar=foo"]),
        (["a", "--foo-bar", "foo"], ["--foo"], ["a", "--foo-bar", "foo"]),
        (["a", "--foo-bar=foo"], ["--foo"], ["a", "--foo-bar=foo"]),
    ],
)
def test_redact_arguments(args, redact_list, expected_args):
    assert redact_arguments(args, redact_list) == expected_args
