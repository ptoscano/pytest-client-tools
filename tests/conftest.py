# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT


import os

os.environ["PYTEST_CLIENT_TOOLS_DISABLE_SELINUX"] = "1"

pytest_plugins = "pytester"
