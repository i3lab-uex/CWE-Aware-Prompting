# -*- coding: utf-8 -*-
"""
Employee record update utility.

This module provides a single function, `update_employee_record`, that safely updates
attributes on an employee dictionary.  It protects against accidental or malicious
modification of sensitive fields such as ``social_security_number`` by restricting
updates to a predefined set of editable keys.  Admin users bypass this restriction.

Security considerations:
- Keys that start with an underscore or contain double underscores are rejected
  to prevent accidental modification of private/internal attributes.
- The function operates on a shallow copy, leaving the original employee object
  unchanged unless explicitly desired.
- The function raises informative exceptions for invalid keys or attempts to modify
  protected fields.

References:
CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
"""

from __future__ import annotations

# Global set of fields that regular users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "salary",
    "department",
}

def _is_valid_field(field: str) -> bool:
    """
    Validate a field name.
    Reject names that start with '_' or contain double underscores to avoid
    accidental modification of private/internal attributes.
    """
    return not (field.startswith("_") or "__" in field)

def update_employee_record(employee: dict, updates: dict, is_admin: bool) -> dict:
    """
    Return a new employee dictionary with the requested updates applied.

    Parameters
    ----------
    employee : dict
        Original employee record.
    updates : dict
        Mapping of field names to new values.
    is_admin : bool
        If True, the caller has administrative privileges and can update any field.
        Otherwise only fields listed in EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If `updates` contains an invalid key or a protected field when the caller is not an admin.
    TypeError
        If `employee` or `updates` are not dictionaries.

    Notes
    -----
    The function does **not** modify the original `employee` dictionary; it returns a new dict.
    """
    if not isinstance(employee, dict):
        raise TypeError(f"employee must be a dict; got {type(employee).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict; got {type(updates).__name__}")

    # Prepare the new record
    updated = employee.copy()

    for key, value in updates.items():
        if not isinstance(key, str):
            raise ValueError(f"Field names must be strings; got {type(key).__name__}")

        if not _is_valid_field(key):
            raise ValueError(f"Invalid field name '{key}': cannot start with '_' or contain '__'")

        if not is_admin and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: field '{key}' cannot be updated by a non-admin user"
            )

        # Perform the update
        updated[key] = value

    return updated