# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT

import contextlib
import functools
import locale
import pathlib
import shutil
import subprocess

import pytest

from .candlepin import Candlepin, ping_candlepin
from .insights_client import InsightsClient, INSIGHTS_CLIENT_FILES_TO_SAVE
from .podman import Podman
from .subscription_manager import (
    SubscriptionManager,
    SUBMAN_FILES_TO_SAVE,
    stop_rhsmcertd,
)
from .rhc import Rhc, RHC_FILES_TO_SAVE
from .test_config import TestConfig


_MARKERS = {
    "candlepin": "tests requiring a self-deployed Candlepin",
    "external_candlepin": "tests requiring an externally deployed Candlepin",
    "any_candlepin": "tests requiring any type of Candlepin",
    "subman": "tests for subscription-manager",
    "insights_client": "tests for insights-client",
    "rhc": "tests for rhc",
}
_CANDLEPIN_FIXTURES = {x for x in _MARKERS.keys() if "candlepin" in x}


def _save_and_archive(files, subdir):
    def decorator_wrapper(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            tmp_path = kwargs["tmp_path"]
            request = kwargs["request"]
            artifacts_path = pathlib.Path.cwd()
            artifacts_path /= "artifacts"
            artifacts_path.mkdir(parents=True, exist_ok=True)
            backup_path = tmp_path / f"backup-{subdir}"
            backup_path.mkdir()
            for f in files:
                with contextlib.suppress(FileNotFoundError):
                    if f.remove_at_start:
                        shutil.move(f.path, backup_path)
                    else:
                        shutil.copy2(f.path, backup_path)
            yield from func(*args, **kwargs)
            if request.module:
                artifacts_path /= request.module.__name__
            if request.cls:
                artifacts_path /= request.cls.__name__
            artifacts_path /= request.node.name
            artifacts_path.mkdir(parents=True, exist_ok=True)
            for f in files:
                with contextlib.suppress(FileNotFoundError):
                    shutil.copy2(f.path, artifacts_path)
                with contextlib.suppress(FileNotFoundError):
                    shutil.move(backup_path / f.path.name, f.path)

        return function_wrapper

    return decorator_wrapper


def _create_candlepin_container():
    return Podman(
        image="ghcr.io/ptoscano/candlepin-unofficial:latest",
        hostname="candlepin.local",
        port_mappings=[[8443, 8443], [8080, 8080]],
    )


@pytest.fixture(scope="session")
def test_config(request):
    return TestConfig(request.config.getoption("--test-config"))


@pytest.fixture(scope="session")
def candlepin(request):
    with contextlib.ExitStack() as stack:
        start_container = not request.config.getoption(
            "--candlepin-container-is-running"
        )
        initial_wait = 0
        if start_container:
            stack.enter_context(_create_candlepin_container())
            # candlepin takes a while to start
            initial_wait = 5
        candlepin = Candlepin(
            host="localhost",
            port=8443,
            prefix="/candlepin",
            insecure=True,
        )
        ping_candlepin(candlepin, initial_wait=initial_wait)
        yield candlepin


@pytest.fixture(scope="session")
def external_candlepin(test_config):
    if not test_config.is_external:
        pytest.skip("missing external candlepin")
    candlepin = Candlepin(
        host=test_config.get("candlepin", "host"),
        port=test_config.get("candlepin", "port"),
        prefix=test_config.get("candlepin", "prefix"),
        insecure=test_config.get("candlepin", "insecure"),
    )
    yield candlepin


@pytest.fixture(scope="session")
def any_candlepin(request, test_config):
    candlepin_fixture = "external_candlepin" if test_config.is_external else "candlepin"
    candlepin = request.getfixturevalue(candlepin_fixture)
    yield candlepin


@pytest.fixture
@_save_and_archive(files=SUBMAN_FILES_TO_SAVE, subdir="subman")
def save_subman_files(tmp_path, request):
    yield


@pytest.fixture
def subman(save_subman_files, test_config):
    subman = SubscriptionManager()
    # TODO enable debug also for all the categories
    subman.config(
        server_hostname="invalid-hostname-set-to-avoid-mistakes",
        logging_default_log_level="DEBUG",
    )
    try:
        yield subman
    finally:
        with contextlib.suppress(subprocess.SubprocessError):
            subman.unregister()
        stop_rhsmcertd()


@pytest.fixture
def _init_subman_from_candlepin(request):
    assert "subman" in request.node.fixturenames
    candlepin_fixture = next(
        (i for i in request.node.fixturenames if i in _CANDLEPIN_FIXTURES),
        None,
    )
    assert candlepin_fixture
    subman = request.getfixturevalue("subman")
    candlepin = request.getfixturevalue(candlepin_fixture)
    subman.config(
        server_hostname=candlepin.host,
        server_port=candlepin.port,
        server_prefix=candlepin.prefix,
        server_insecure="1" if candlepin.insecure else "0",
    )


@pytest.fixture
@_save_and_archive(files=INSIGHTS_CLIENT_FILES_TO_SAVE, subdir="insights-client")
def save_insights_client_files(tmp_path, request):
    yield


@pytest.fixture
def insights_client(save_insights_client_files):
    insights_client = InsightsClient()
    try:
        yield insights_client
    finally:
        with contextlib.suppress(subprocess.SubprocessError):
            insights_client.unregister()


@pytest.fixture
@_save_and_archive(files=RHC_FILES_TO_SAVE, subdir="rhc")
def save_rhc_files(tmp_path, request):
    yield


@pytest.fixture
def rhc(save_rhc_files, test_config):
    rhc = Rhc()
    try:
        yield rhc
    finally:
        with contextlib.suppress(subprocess.SubprocessError):
            rhc.disconnect()


def pytest_addoption(parser):
    group = parser.getgroup("client-tools")
    group.addoption(
        "--test-config", action="store", type=pathlib.Path, help="custom test config"
    )
    group.addoption(
        "--candlepin-container-is-running",
        action="store_true",
        help="the container of Candlepin is already running",
    )


def pytest_collection_modifyitems(config, items):
    for item in items:
        markers_to_add = set()
        item_markers = {m.name for m in item.own_markers}
        for fixture_name in item.fixturenames:
            if fixture_name not in _MARKERS:
                # fixture without associated marker, skip
                continue
            if fixture_name not in item_markers:
                markers_to_add.add(fixture_name)
        for marker in markers_to_add:
            item.add_marker(marker)
        if "rhc" in item.fixturenames:
            if "subman" not in item.fixturenames:
                item.fixturenames.append("subman")
            if "insights_client" not in item.fixturenames:
                item.fixturenames.append("insights_client")
        if "subman" in item.fixturenames and any(
            i in item.fixturenames for i in _CANDLEPIN_FIXTURES
        ):
            item.fixturenames.append("_init_subman_from_candlepin")
        for jira_marker in item.iter_markers(name="jira"):
            for jira in jira_marker.args:
                jira_item = jira.lower()
                jira_item = jira_item.replace("-", "_")
                jira_item = "jira_" + jira_item
                item.add_marker(jira_item)
                config.addinivalue_line(
                    "markers", f"{jira_item}: test for jira card {jira}"
                )


def pytest_configure(config):
    for mark, description in _MARKERS.items():
        config.addinivalue_line("markers", f"{mark}: {description}")
    config.addinivalue_line("markers", "jira(id): test for jira cards")
    locale.setlocale(locale.LC_ALL, "C.UTF-8")
