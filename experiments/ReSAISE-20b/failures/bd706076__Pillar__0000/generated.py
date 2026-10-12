#!/usr/bin/env python3
"""
Utility module for updating employee records.

The `update_employee_record` function ensures that only allowed fields are
modified unless the caller has administrative privileges.  It operates on a
dictionary representation of an employee and returns a new dictionary with the
applied updates, leaving the original object untouched.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated by
avoiding side‑effects on the input dictionary and by explicitly creating a new
resource (the updated dict) before returning it.  The function does not hold
any persistent state beyond the local scope, thus preventing accidental
resource leakage or misuse.
"""

from copy import deepcopy
from typing import Dict

# Fields that a regular user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def update_employee_record(
    employee: Dict[str, any],
    updates: Dict[str, any],
    is_admin: bool = False
) -> Dict[str, any]:
    """
    Update an employee record with the supplied changes.

    Parameters
    ----------
    employee : dict
        Original employee data.  Must contain at least the keys:
        'name', 'position', 'salary', 'department', 'social_security_number'.
    updates : dict
        Mapping of fields to new values.
    is_admin : bool, optional
        If True, the caller may modify any field; otherwise only fields in
        EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If `updates` contains a field that the caller is not permitted to modify.
    KeyError
        If `employee` lacks any of the mandatory keys.
    TypeError
        If input arguments are not dictionaries.

    Notes
    -----
    - The function does **not** modify the original `employee` dictionary.
      Instead, it returns a new dict with the updates applied.
    - The function performs shallow copying of nested objects.  If deep copies
      are required for complex structures, adjust the implementation accordingly.
    """
    # Basic type checks
    if not isinstance(employee, dict):
        raise TypeError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Ensure mandatory keys exist in the employee record
    required_keys = {"name", "position", "salary", "department",
                     "social_security_number"}
    missing = required_keys - employee.keys()
    if missing:
        raise KeyError(f"Missing mandatory keys in employee record: {missing}")

    # Start with a deep copy to avoid modifying the original
    updated = deepcopy(employee)

    for field, new_value in updates.items():
        # Admins can modify any field; regular users are restricted
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(f"Field '{field}' cannot be updated by non‑admin user")

        # Apply the update
        updated[field] = new_value

    return updated