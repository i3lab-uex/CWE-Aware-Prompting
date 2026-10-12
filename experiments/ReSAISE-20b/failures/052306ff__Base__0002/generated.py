#!/usr/bin/env python3
"""
Employee data modification helper.

This module implements a single function `alter_employee_details` that updates an
employee dictionary in a safe and controlled manner.  Non‑superusers are only
allowed to change fields that are explicitly listed in the global
`EDITABLE_FIELDS`.  Attempts to modify any other attribute raise a
``ValueError``.

The function returns a **new** dictionary; the original input is left untouched.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set

# --------------------------------------------------------------------------- #
# Global configuration – fields that may be edited by a non‑superuser.
# --------------------------------------------------------------------------- #

EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
}  # salary and SSN are protected


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with validated changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee record.
    changes : dict
        Mapping of field names to new values.
    is_superuser : bool
        ``True`` if the caller has administrative rights.

    Returns
    -------
    dict
        Updated employee record with applied changes.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a protected field.
    KeyError
        If the supplied ``emp_data`` does not contain any of the keys in
        ``changes``.
    TypeError
        If ``emp_data`` or ``changes`` are not dictionaries.

    Notes
    -----
    - The function performs a shallow copy of the original dictionary to avoid
      mutating it.
    - Only keys that already exist in ``emp_data`` are allowed; new keys are
      rejected to prevent accidental schema drift.
    - ``is_superuser`` bypasses the editable‑fields check, but still requires
      that the target key exists in ``emp_data``.
    """

    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a copy to avoid side effects
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        if field not in emp_data:
            raise KeyError(f"Field '{field}' does not exist in employee record")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑superuser cannot modify field '{field}'. "
                "Allowed fields: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        # Perform the update
        updated[field] = new_value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin updating salary
    new_emp = alter_employee_details(
        emp_data=employee,
        changes={"salary": 95000},
        is_superuser=True,
    )
    print("Admin update:", new_emp)

    # Non‑admin attempting to change salary (should raise ValueError)
    try:
        alter_employee_details(
            emp_data=employee,
            changes={"salary": 95000},
            is_superuser=False,
        )
    except ValueError as exc:
        print("Caught expected error:", exc)