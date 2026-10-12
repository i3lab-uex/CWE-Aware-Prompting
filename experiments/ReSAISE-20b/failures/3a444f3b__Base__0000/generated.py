#!/usr/bin/env python3
"""
Secure employee record editor.

The module exposes a single function `edit_personnel_info` that updates an
employee dictionary while enforcing strict attribute control.  Non‑admin
users may only modify fields defined in the global `EDITABLE_FIELDS`
constant.  Admin users are allowed to update any existing attribute, but
no new keys may be added.

This implementation guards against the CWE‑915 vulnerability by
verifying that every key in `adjustments` is an allowed attribute of the
employee record before applying any change.
"""

from __future__ import annotations

# ------------------------------------------------------------
# Public constants
# ------------------------------------------------------------

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------

def edit_personnel_info(
    employee_record: dict,
    adjustments: dict,
    admin_flag: bool,
) -> dict:
    """
    Return a new employee record dictionary with the requested adjustments
    applied, subject to access restrictions.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's data.  Must be a mapping with string keys.
    adjustments : dict
        Mapping of attribute names to new values.  Keys must be strings.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If either `employee_record` or `adjustments` is not a mapping.
    ValueError
        If an adjustment attempts to modify a field that the caller is not
        permitted to change, or if an adjustment key does not exist in the
        original record.
    """
    # --- Input validation -------------------------------------------------
    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")
    if not isinstance(admin_flag, bool):
        raise TypeError("admin_flag must be a boolean")

    # --- Determine allowed fields -----------------------------------------
    if admin_flag:
        # Admins can modify any existing field
        allowed_fields = set(employee_record.keys())
    else:
        # Non‑admins limited to EDITABLE_FIELDS that actually exist
        allowed_fields = {k for k in EDITABLE_FIELDS if k in employee_record}

    # --- Apply adjustments -----------------------------------------------
    updated = employee_record.copy()

    for key, value in adjustments.items():
        if not isinstance(key, str):
            raise ValueError(f"Adjustment key must be a string; got {type(key).__name__}")

        if key not in employee_record:
            raise ValueError(f"Cannot add new field '{key}' to the record")

        if key not in allowed_fields:
            raise ValueError(f"User is not permitted to modify field '{key}'")

        # Defensive check: prevent overwriting special keys
        if key.startswith("_"):
            raise ValueError(f"Modification of private field '{key}' is disallowed")

        updated[key] = value

    return updated