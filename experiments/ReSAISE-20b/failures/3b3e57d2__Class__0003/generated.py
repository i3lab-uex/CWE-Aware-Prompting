#!/usr/bin/env python3
"""
Safe employee detail modification utility.

The function `modify_staff_details` updates an employee record
according to the supplied changes while respecting
the permissions of the user performing the update.
"""

from typing import Dict, Any

# Fields that a regular (non‑superuser) employee is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}


def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Update an employee's details with the supplied changes.

    Parameters
    ----------
    employee_data : dict
        Current attributes of the employee.
    changes : dict
        Proposed modifications to apply.
    is_superuser : bool
        Flag indicating whether the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a protected field,
        or if the changes reference unknown keys.
    """

    # Defensive copy to avoid mutating input
    updated = employee_data.copy()

    for key, new_value in changes.items():
        # Ensure the field exists on the employee record
        if key not in updated:
            raise ValueError(f"Unknown field '{key}' cannot be modified.")

        # Enforce edit permissions
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify field '{key}'."
            )

        # Apply the change
        updated[key] = new_value

    return updated