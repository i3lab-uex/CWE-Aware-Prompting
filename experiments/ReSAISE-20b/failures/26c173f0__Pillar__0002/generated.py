#!/usr/bin/env python3
"""
AccessControl – secure string formatting for user information.

The :func:`format_string` function safely formats a string that may contain
references to attributes of a :class:`UserInfo` instance.  Only the two
attributes ``user_name`` and ``user_password`` are allowed; any other
references raise a :class:`ValueError`.  This protects against unintended
access to internal state and mitigates the risk of leaking sensitive data.

CWE-664: Improper Control of a Resource Through its Lifetime
------------------------------------------------------------
This module does not allocate any external resources (files, sockets,
etc.) and therefore has no lifetime to manage.  The only resource
handled is the :class:`UserInfo` instance, which is created and released
within the function call, guaranteeing proper cleanup.
"""

from __future__ import annotations

import string
from dataclasses import dataclass


@dataclass(frozen=True)
class UserInfo:
    """Simple container for user credentials."""
    user_name: str
    user_password: str


class _SafeFormatter(string.Formatter):
    """
    A :class:`string.Formatter` that only permits formatting of the
    ``userinfo`` placeholder and disallows any other fields or attribute
    access.
    """

    _ALLOWED_FIELDS = {"userinfo.user_name", "userinfo.user_password"}

    def get_value(self, key: object, args: tuple, kwargs: dict) -> object:
        # ``key`` can be an integer (positional index) or a string
        if isinstance(key, int):
            # Positional arguments are not allowed.
            raise ValueError("Positional formatting is disallowed.")
        if key in ("userinfo",):
            # ``{userinfo}`` alone is not allowed; must reference an attribute.
            raise ValueError("Direct access to 'userinfo' without an attribute is disallowed.")
        if key in self._ALLOWED_FIELDS:
            # Resolve the attribute safely.
            obj_name, attr = key.split(".", 1)
            if obj_name != "userinfo":
                raise ValueError(f"Invalid object name: {obj_name!r}")
            userinfo = kwargs.get("userinfo")
            if not isinstance(userinfo, UserInfo):
                raise ValueError("'userinfo' placeholder missing or invalid.")
            return getattr(userinfo, attr)
        # Any other key is forbidden.
        raise ValueError(f"Disallowed format field: {key!r}")

    def get_field(self, field_name: str, args: tuple, kwargs: dict):
        """
        Override to ensure that nested fields are resolved correctly.
        """
        # The default implementation already calls get_value, so we simply
        # delegate to it after checking the field name.
        if field_name not in self._ALLOWED_FIELDS:
            raise ValueError(f"Disallowed format field: {field_name!r}")
        return self.get_value(field_name, args, kwargs), None


def format_string(string: str) -> str:
    """
    Safely format a string containing placeholders for user information.

    Parameters
    ----------
    string : str
        The format string.  It may contain placeholders such as
        ``{userinfo.user_name}`` or ``{userinfo.user_password}``.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the format string contains disallowed fields or if formatting fails.
    """
    try:
        formatter = _SafeFormatter()
        # Instantiate a dummy UserInfo; in real usage this would be replaced
        # with actual user data.  For demonstration, use placeholder values.
        dummy_user = UserInfo(user_name="alice", user_password="secret")
        return formatter.format(string, userinfo=dummy_user)
    except Exception as exc:
        # Wrap any exception in ValueError for a consistent API.
        raise ValueError(f"Error formatting string: {exc}") from exc