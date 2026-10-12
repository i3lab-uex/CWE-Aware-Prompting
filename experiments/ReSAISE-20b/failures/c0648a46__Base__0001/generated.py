#!/usr/bin/env python3
"""
Employee profile modification utility.

The function `modify_employee_profile` safely updates an employee's profile
dictionary based on a set of proposed changes. Non‑privileged users are only
allowed to edit fields listed in the global `EDITABLE_FIELDS` constant, while
privileged (admin) users can modify any field. The implementation protects
against the CWE‑915 vulnerability by strictly controlling which attributes
may be altered.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Fields that non‑admin users may modify.  Adjust as needed.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other safe-to-edit fields here.
}


def _validate_changes(changes: Dict[str, Any]) -> None:
    """
    Ensure that the changes dictionary is well‑formed.

    Raises:
        TypeError: If `changes` is not a dict or contains non‑string keys.
    """
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")
    for key in changes:
        if not isinstance(key, str):
            raise TypeError(f"Change keys must be strings; got {type(key).__name__}")


def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker : dict
        Current employee profile.  Keys are attribute names, values are the
        corresponding data.
    changes : dict
        Proposed updates.  Keys are attribute names, values are the new data.
    is_privileged : bool
        If ``True`` the caller has admin rights and may modify any field.
        Otherwise only fields in :data:`EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A shallow copy of ``worker`` with the permitted updates applied.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify a disallowed field.
    TypeError
        If the input arguments are of incorrect type.

    Notes
    -----
    The function does **not** modify the original ``worker`` dictionary.
    """
    if not isinstance(worker, dict):
        raise TypeError("`worker` must be a dictionary")
    _validate_changes(changes)

    # Create a shallow copy so the original dict remains unchanged.
    updated_profile = copy.deepcopy(worker)

    for field, new_value in changes.items():
        # Check privilege
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑privileged users cannot modify the field: '{field}'."
            )

        # Only update if the field exists in the original profile.
        if field not in updated_profile:
            # For security we skip unknown fields; alternatively raise an error.
            continue

        updated_profile[field] = new_value

    return updated_profile