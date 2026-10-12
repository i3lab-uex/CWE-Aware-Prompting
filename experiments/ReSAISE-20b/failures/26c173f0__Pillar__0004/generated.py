#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AccessControl – format_string helper

This module implements a safe formatting routine that can only interpolate
the `user_name` and `user_password` attributes of a :class:`UserInfo`
instance.  Any attempt to format using other keys, or any formatting
error, results in a :class:`ValueError`.

The implementation uses :func:`string.Formatter.parse` to inspect the
format string and guarantees that only the allowed fields are present.
"""

import string
from dataclasses import dataclass

__all__ = ["UserInfo", "format_string"]


@dataclass(frozen=True)
class UserInfo:
    """
    Simple container for user credentials.
    The attributes are immutable to avoid accidental mutation.
    """
    user_name: str
    user_password: str


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_format_string(fmt: str) -> None:
    """
    Ensure that *fmt* contains only the permitted format fields
    (`userinfo.user_name` and `userinfo.user_password`).  Raises a
    :class:`ValueError` if any other field is found.
    """
    allowed = {"userinfo.user_name", "userinfo.user_password"}
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(fmt):
        if field_name is None:
            continue
        # In the allowed syntax, the field name must be exactly one of the two
        if field_name not in allowed:
            raise ValueError(f"Forbidden format field: {field_name!r}")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def format_string(fmt: str, userinfo: UserInfo) -> str:
    """
    Safely format *fmt* using the supplied :class:`UserInfo` instance.

    Parameters
    ----------
    fmt:
        The format string that may contain `{userinfo.user_name}` or
        `{userinfo.user_password}` placeholders.
    userinfo:
        An instance of :class:`UserInfo` whose attributes are injected into
        the format string.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the format string contains disallowed fields, or if formatting
        fails for any reason.
    """
    if not isinstance(fmt, str):
        raise ValueError("format_string expects a string as the first argument")

    if not isinstance(userinfo, UserInfo):
        raise ValueError("format_string expects a UserInfo instance as the second argument")

    # Validate that the format string only contains allowed fields
    _validate_format_string(fmt)

    try:
        # Perform the actual formatting
        return fmt.format(userinfo=userinfo)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception into ValueError for a consistent API
        raise ValueError(f"Formatting failed: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove to use in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Demo user
    demo_user = UserInfo(user_name="alice", user_password="s3cr3t")

    # Valid format
    print(format_string("Hello, {userinfo.user_name}!", demo_user))

    # Invalid format – will raise ValueError
    try:
        print(format_string("Password: {userinfo.user_password}", demo_user))
    except ValueError as e:
        print(f"Error: {e}")