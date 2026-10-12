#!/usr/bin/env python3
"""
Secure staff record modification utility.
"""

from copy import deepcopy
from typing import Dict

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

# Fields that are considered sensitive and require admin privileges.
SENSITIVE_FIELDS = {"salary", "social_security_number"}


def modify_staff_info(
    staff: Dict[str, any],
    changes: Dict[str, any],
    admin_status: bool,
) -> Dict[str, any]:
    """
    Return an updated copy of *staff* applying *changes* safely.

    Parameters
    ----------
    staff : dict
        Current employee record. Must contain at least the keys referenced in
        *changes*.
    changes : dict
        Proposed field updates. Keys are field names, values are new data.
    admin_status : bool
        ``True`` if the caller has administrative privileges, otherwise
        ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a disallowed field, or if a field
        is missing from the original record.

    Notes
    -----
    * The function never mutates the input ``staff`` dictionary; it returns a
      shallow copy with changes applied.
    * Only keys present in the original record can be updated; attempting to
      add a new key raises an error.
    * Sensitive fields are only modifiable by admins.
    """
    # Create a shallow copy to avoid side effects on the original data
    updated = deepcopy(staff)

    for key, new_value in changes.items():
        # Ensure the field exists in the original record
        if key not in staff:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")

        # Determine if the user has permission to modify this field
        if not admin_status:
            if key in SENSITIVE_FIELDS:
                raise ValueError(
                    f"Insufficient privileges to modify sensitive field '{key}'."
                )
            if key not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Field '{key}' is not editable by non‑admin users."
                )

        # Apply the change
        updated[key] = new_value

    return updated


# Example usage (for testing only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change position and salary
    try:
        result = modify_staff_info(
            staff=employee,
            changes={"position": "Senior Engineer", "salary": 90000},
            admin_status=False,
        )
    except ValueError as e:
        print(f"Permission error: {e}")

    # Admin changing salary
    updated = modify_staff_info(
        staff=employee,
        changes={"salary": 90000},
        admin_status=True,
    )
    print(updated)