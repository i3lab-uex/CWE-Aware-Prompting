#!/usr/bin/env python3
"""
Utility to safely modify employee details with role‑based field restrictions.
"""

from __future__ import annotations

import copy
from typing import Dict, Set


# --------------------------------------------------------------------------- #
# Global configuration: fields that a non‑superuser is allowed to edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Add more safe, non‑sensitive fields here.
}


def _validate_changes(
    changes: Dict[str, any],
    is_superuser: bool,
) -> None:
    """
    Ensure that all proposed changes are permitted for the current user.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a restricted field.
    """
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    for key in changes:
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Unauthorized modification attempt on field '{key}'. "
                "Insufficient privileges."
            )


def modify_staff_details(
    employee_data: Dict[str, any],
    changes: Dict[str, any],
    is_superuser: bool,
) -> Dict[str, any]:
    """
    Return a new employee dictionary with the requested modifications applied.

    Parameters
    ----------
    employee_data : dict
        Current attributes of an employee.
    changes : dict
        Proposed updates. Keys must be valid attribute names.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A copy of ``employee_data`` with the changes applied.

    Raises
    ------
    TypeError
        If inputs are of incorrect type.
    ValueError
        If a non‑superuser attempts to modify restricted fields.

    Notes
    -----
    - The original ``employee_data`` dictionary is **not** mutated.
    - Only keys present in ``changes`` are updated; all other attributes remain
      untouched.
    """
    if not isinstance(employee_data, dict):
        raise TypeError("`employee_data` must be a dictionary")

    # Ensure changes are valid for the current role
    _validate_changes(changes, is_superuser)

    # Work on a shallow copy to avoid side‑effects; deepcopy if nested objects
    updated = copy.deepcopy(employee_data)

    # Apply changes
    for key, value in changes.items():
        updated[key] = value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (commented out; remove for production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 90000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Superuser attempting to change salary and SSN
    super_changes = {"salary": 95000, "social_security_number": "987-65-4321"}
    print(
        modify_staff_details(employee, super_changes, is_superuser=True)
    )

    # Regular user attempting to change position (allowed) and salary (not allowed)
    try:
        user_changes = {"position": "Senior Engineer", "salary": 100000}
        print(modify_staff_details(employee, user_changes, is_superuser=False))
    except ValueError as exc:
        print(f"Permission error: {exc}")