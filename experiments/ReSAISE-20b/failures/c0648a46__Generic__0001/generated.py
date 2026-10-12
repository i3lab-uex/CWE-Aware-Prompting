#!/usr/bin/env python3
"""
Utility to modify an employee profile while enforcing edit permissions.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Fields that non‑admin users are allowed to modify
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Add other fields that are safe for non‑admin editing
}


def _validate_changes(changes: Dict[str, Any], is_privileged: bool) -> None:
    """
    Validate that the changes dictionary contains only allowed fields.
    Raises ValueError if a forbidden field is present for non‑privileged users.
    """
    if is_privileged:
        # Admins may modify any field
        return

    forbidden = set(changes) - EDITABLE_FIELDS
    if forbidden:
        raise ValueError(
            f"Non‑privileged users cannot modify the following fields: {', '.join(sorted(forbidden))}"
        )


def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the specified changes applied.

    Parameters
    ----------
    worker : dict
        The original employee profile. Keys represent field names.
    changes : dict
        Mapping of fields to new values that should be applied.
    is_privileged : bool
        True if the caller has administrative privileges; otherwise False.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify a field that is not in
        :data:`EDITABLE_FIELDS`.
    """
    # Ensure we don't mutate the caller's dictionary
    updated_profile = copy.deepcopy(worker)

    # Validate changes before applying them
    _validate_changes(changes, is_privileged)

    # Apply the allowed changes
    for field, new_value in changes.items():
        updated_profile[field] = new_value

    return updated_profile