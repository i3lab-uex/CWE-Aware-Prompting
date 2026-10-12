#!/usr/bin/env python3
"""
Secure employee profile updater.

This module provides a single public function:
    adjust_employee_profile(emp, changes, has_admin_rights)

The function ensures that only a predefined set of fields can be modified by
regular users, while administrators have full editing rights.

Security considerations:
- CWE‑915: Improperly Controlled Modification of Dynamically‑Determined Object Attributes
  is mitigated by explicitly validating field names against a whitelist.
- Input types are validated to avoid accidental injection of malicious objects.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Global whitelist of fields that can be edited by non‑admin users.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Add other safe fields here.
}


def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with requested changes applied.

    Parameters
    ----------
    emp : dict
        The original employee record. Must be a mapping of attribute names to values.
    changes : dict
        Proposed modifications keyed by attribute name. Values can be any JSON‑serialisable type.
    has_admin_rights : bool
        True if the caller is an administrator; otherwise False.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    TypeError
        If ``emp`` or ``changes`` is not a dictionary.
    ValueError
        If a non‑admin attempts to modify a field outside ``EDITABLE_FIELDS``.
    """
    if not isinstance(emp, dict):
        raise TypeError(f"emp must be a dict, got {type(emp).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict, got {type(changes).__name__}")

    # Create a shallow copy to avoid mutating the original employee record.
    updated_emp = copy.deepcopy(emp)

    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise TypeError(f"Field names must be strings; got {type(field).__name__}")

        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify '{field}' without administrative rights."
            )

        # Perform the update
        updated_emp[field] = new_value

    return updated_emp


# Example usage (uncomment to test)
if __name__ == "__main__":
    employee = {
        "name": "Alice",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {
        "position": "Senior Developer",
        "salary": 95000,            # Not editable by regular users
    }

    try:
        # Regular user attempt
        print(adjust_employee_profile(employee, changes, has_admin_rights=False))
    except Exception as e:
        print(f"Error: {e}")

    # Admin user
    updated = adjust_employee_profile(employee, changes, has_admin_rights=True)
    print(updated)