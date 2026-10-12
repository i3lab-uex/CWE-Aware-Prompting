#!/usr/bin/env python3
"""
Module providing a safe edit routine for personnel records.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary can be edited by admins only; include it here for completeness.
    "salary",
}


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return a new employee record with the requested adjustments applied.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Mapping of field names to new values.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a non‑editable field or if the
        supplied employee record lacks required keys.
    """
    # Ensure we do not mutate the original dictionary
    updated = deepcopy(employee_record)

    # Validate that the employee record contains expected mandatory fields
    required_keys = {"name", "position", "department", "salary", "social_security_number"}
    missing = required_keys - employee_record.keys()
    if missing:
        raise ValueError(f"Employee record is missing required keys: {missing}")

    # Process each adjustment
    for field, new_value in adjustments.items():
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise ValueError(f"Non‑admin users cannot edit the '{field}' field.")

        # Basic type checks: reject None values for required fields
        if field in required_keys and new_value is None:
            raise ValueError(f"Field '{field}' cannot be set to None.")

        # Apply the change
        updated[field] = new_value

    return updated