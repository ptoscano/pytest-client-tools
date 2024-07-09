# SPDX-FileCopyrightText: Red Hat
# SPDX-License-Identifier: MIT


class SystemNotRegisteredError(RuntimeError):
    """
    The system is not registered.
    """

    def __init__(self):
        pass
