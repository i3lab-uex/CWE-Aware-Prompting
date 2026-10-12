#!/usr/bin/env python3
"""
Utility to safely modify employee records.

The function enforces that only whitelisted fields may be edited by
non‑superusers.  Superusers are allowed to modify any field.
"""

from __future__ import annotations

from typing import Dict, Any, Set


# Fields that regular users are permitted to edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}


def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary after applying the requested changes.

    Parameters
    ----------
    employee_data : dict
        Original employee record.
    changes : dict
        Proposed modifications.  Keys are attribute names, values are new values.
    is_superuser : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    PermissionError
        If a non‑superuser attempts to modify a field not in EDITABLE_FIELDS.
    ValueError
        If `employee_data` or `changes` is not a dictionary.
    """
    if not isinstance(employee_data, dict):
        raise ValueError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise ValueError("changes must be a dictionary")

    # Enforce field-level permissions
    if not is_superuser:
        disallowed = set(changes) - EDITABLE_FIELDS
        if disallowed:
            raise PermissionError(
                f"Non‑superuser cannot modify fields: {', '.join(sorted(disallowed))}"
            )

    # Create a shallow copy to avoid mutating the original
    updated = employee_data.copy()
    for key, value in changes.items():
        # Avoid adding keys that were not present originally if the policy demands it
        updated[key] = value

    return updated