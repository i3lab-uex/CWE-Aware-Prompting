# -*- coding: utf-8 -*-
"""
Utility to safely edit an employee record.

This module implements the `edit_personnel_info` function which
allows modifications to a personnel dictionary while enforcing
restrictions on which fields may be edited by non‑admin users.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that can be edited by non‑admin users.
EDITABLE_FIELDS = {"name", "position", "department"}


def _validate_adjustments(adjustments: Dict[str, Any]) -> None:
    """
    Ensure that the adjustments argument is a dictionary and
    contains only hashable keys. Raises TypeError if validation fails.
    """
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")

    for key in adjustments:
        if not isinstance(key, str):
            raise TypeError(f"Adjustment key {key!r} is not a string")


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return an updated copy of *employee_record* with the supplied
    *adjustments* applied.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key/value pairs for fields to update.
    admin_flag : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    TypeError
        If `adjustments` is not a dictionary or contains non‑string keys.
    ValueError
        If a non‑admin attempts to modify a restricted field.
    """
    # Defensive copy so the original record is not mutated
    updated_record = deepcopy(employee_record)

    _validate_adjustments(adjustments)

    for field, new_value in adjustments.items():
        # Reject attempts to change read‑only or sensitive fields
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_record[field] = new_value

    return updated_record


# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     emp = {
#         "name": "Alice",
#         "position": "Developer",
#         "salary": 90000,
#         "department": "Engineering",
#         "social_security_number": "123-45-6789"
#     }
#
#     changes = {"salary": 95000, "department": "R&D"}
#     print(edit_personnel_info(emp, changes, admin_flag=False))