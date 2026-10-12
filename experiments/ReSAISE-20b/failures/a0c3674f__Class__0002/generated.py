#!/usr/bin/env python3
"""
Utility for safely modifying staff records.

The module defines a global set of fields that non‑admin users are allowed to edit.
Attempting to modify any other field will raise a ValueError.  Admin users can
modify all fields.

The implementation avoids dynamic code execution and ensures that the input data
are not mutated in place by returning a new dictionary instance.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Iterable


# Fields that can be edited by non‑admin users.
EDITABLE_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "position",
        "department",
        # Note: salary and social_security_number are protected.
    }
)


def _validate_changes(
    changes: Dict[str, Any],
    editable_fields: Iterable[str] | None = None,
) -> None:
    """
    Validate that all keys in `changes` are allowed.

    Raises
    ------
    ValueError
        If any key is not in `editable_fields`.
    """
    if editable_fields is None:
        return

    invalid_keys = [k for k in changes if k not in editable_fields]
    if invalid_keys:
        raise ValueError(
            f"Attempt to modify restricted fields: {', '.join(invalid_keys)}"
        )


def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return an updated staff dictionary after applying allowed changes.

    Parameters
    ----------
    staff : dict
        The original employee record.
    changes : dict
        Dictionary of field updates. Keys must be valid fields for the user role.
    admin_status : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated staff record.

    Raises
    ------
    ValueError
        If `changes` contains a key that the user is not allowed to modify.
    TypeError
        If `staff` or `changes` are not dictionaries.

    Notes
    -----
    - The function performs a shallow copy of the staff dictionary to avoid
      mutating the caller's data.
    - No evaluation or execution of arbitrary code occurs; only dictionary
      assignments are performed.
    """
    if not isinstance(staff, dict):
        raise TypeError("`staff` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Determine which fields are editable for the current user.
    allowed_fields = None if admin_status else EDITABLE_FIELDS
    _validate_changes(changes, editable_fields=allowed_fields)

    # Create a shallow copy to avoid side effects.
    updated_staff = copy.copy(staff)

    for key, value in changes.items():
        # No special handling of nested structures; direct assignment.
        updated_staff[key] = value

    return updated_staff