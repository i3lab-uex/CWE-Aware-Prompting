# -*- coding: utf-8 -*-
"""
Utility to safely update employee records while preventing unauthorized field modifications.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool = False
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested updates applied.

    Parameters
    ----------
    employee : dict
        Original employee record. Expected keys include:
            - name (str)
            - position (str)
            - salary (float/int)
            - department (str)
            - social_security_number (str)

    updates : dict
        Mapping of fields to new values. Only keys listed in `EDITABLE_FIELDS`
        are allowed for non‑admin users. Admins may modify any field.

    is_admin : bool, optional
        Flag indicating whether the caller has administrative privileges.
        Defaults to False.

    Returns
    -------
    dict
        A shallow copy of `employee` with the specified updates applied.

    Raises
    ------
    TypeError
        If `employee` or `updates` is not a dictionary.

    ValueError
        If an update attempts to modify a non‑editable field without admin rights,
        or if the field does not exist in the employee record.
    """
    # Validate input types
    if not isinstance(employee, dict):
        raise TypeError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_employee = deepcopy(employee)

    for field, new_value in updates.items():
        # Check that the field exists in the employee record
        if field not in updated_employee:
            raise ValueError(f"Field '{field}' does not exist in the employee record")

        # Enforce editable field restrictions for non‑admin users
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Unauthorized update attempt on non‑editable field '{field}'"
            )

        # Apply the update
        updated_employee[field] = new_value

    return updated_employee