#!/usr/bin/env python3
"""
Employee record update helper.

This module defines the `alter_employee_details` function, which safely updates
an employee's record.  Non‑admin users are limited to changing only the fields
listed in `EDITABLE_FIELDS`.  The function validates input keys, protects
against accidental or malicious modification of private attributes,
and returns a new dictionary instance containing the updated data.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: fields that a non‑admin user is allowed to edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}  # Add or remove fields as needed


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.  Must be a mapping.
    changes : dict
        Desired updates as key/value pairs.  Keys must exist in ``emp_data``.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A shallow copy of ``emp_data`` with the applied changes.

    Raises
    ------
    ValueError
        If a requested field does not exist in ``emp_data`` or if a non‑admin
        attempts to modify a disallowed field.
    TypeError
        If ``emp_data`` or ``changes`` is not a mapping type.

    Notes
    -----
    * The function does **not** modify the original ``emp_data`` dictionary.
      It returns a new instance, preserving immutability of input data.
    * Private or protected keys (starting with an underscore) are ignored
      to mitigate accidental leakage of internal state.
    """
    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid side effects
    updated = copy.copy(emp_data)

    for field, new_value in changes.items():
        # Disallow modifying private attributes
        if field.startswith("_"):
            raise ValueError(f"Modification of private attribute '{field}' is prohibited")

        if field not in emp_data:
            raise ValueError(f"Field '{field}' does not exist in the employee record")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated[field] = new_value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Engineer", "salary": 95000}
    try:
        # As a non‑admin user
        updated_emp = alter_employee_details(employee, changes, is_superuser=False)
    except ValueError as exc:
        print(f"Update failed: {exc}")

    # As an admin user
    updated_emp_admin = alter_employee_details(employee, changes, is_superuser=True)
    print("Admin update:", updated_emp_admin)