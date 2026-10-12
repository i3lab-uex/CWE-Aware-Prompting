# -*- coding: utf-8 -*-
"""
Module: personnel_editor

Provides a secure function for editing employee records.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: salary and social_security_number are protected.
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
        Desired changes, mapping field names to new values.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.
    
    Raises
    ------
    ValueError
        If an adjustment attempts to modify a protected field without admin rights.
    """
    # Make a shallow copy; nested structures are left untouched
    updated_record = deepcopy(employee_record)

    for field, new_value in adjustments.items():
        if not admin_flag:
            # Non‑admin users can only modify the fields in EDITABLE_FIELDS
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Insufficient privileges to modify '{field}'. "
                    "Only the following fields are editable: "
                    f"{', '.join(sorted(EDITABLE_FIELDS))}."
                )
        # Apply the change
        updated_record[field] = new_value

    return updated_record