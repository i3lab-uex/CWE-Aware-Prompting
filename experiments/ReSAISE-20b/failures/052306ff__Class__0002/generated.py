#!/usr/bin/env python3
"""
Utility module for employee record modification.

The module provides a single function `alter_employee_details` that updates an
employee dictionary with new values while enforcing strict access control.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Fields that non‑superuser accounts are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary based on the supplied changes.

    Parameters
    ----------
    emp_data : dict
        The current employee record.  It must be a mapping of field names to values.
    changes : dict
        Mapping of fields to the new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative privileges; otherwise
        ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If ``changes`` contains a field that the caller is not permitted to modify.
    TypeError
        If ``emp_data`` or ``changes`` are not dictionaries.

    Notes
    -----
    * The function does **not** modify the original ``emp_data`` dictionary.
      A shallow copy is returned; nested mutable objects are preserved as
      references to the original objects.
    * Only keys that already exist in ``emp_data`` are considered for
      modification.  New keys are ignored to avoid accidental schema drift.
    * No dynamic code execution is performed, preventing CWE‑913
      (Improper Control of Dynamically-Managed Code Resources).
    """
    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the caller's data
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        # Skip fields that do not exist in the original record
        if field not in emp_data:
            continue

        # Enforce edit permissions
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify '{field}'. "
                "Only editable fields are allowed for non-superusers."
            )

        # Apply the change
        updated[field] = new_value

    return updated


# Example usage (commented out – remove comments to run):
#
# if __name__ == "__main__":
#     employee = {
#         "name": "Alice Smith",
#         "position": "Engineer",
#         "salary": 85000,
#         "department": "R&D",
#         "social_security_number": "123-45-6789"
#     }
#
#     # Non-admin attempting to change salary (should raise ValueError)
#     try:
#         alter_employee_details(employee, {"salary": 90000}, is_superuser=False)
#     except ValueError as e:
#         print(e)
#
#     # Admin changing salary
#     updated_emp = alter_employee_details(employee, {"salary": 90000}, is_superuser=True)
#     print(updated_emp)