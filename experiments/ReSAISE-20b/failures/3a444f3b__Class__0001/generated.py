#!/usr/bin/env python3
"""
Utility module for editing employee records safely.
"""

from copy import deepcopy
from typing import Dict

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def edit_personnel_info(
    employee_record: Dict[str, any],
    adjustments: Dict[str, any],
    admin_flag: bool,
) -> Dict[str, any]:
    """
    Update an employee record with the supplied adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key‑value pairs for fields to be updated.
    admin_flag : bool
        If True, the caller has administrative privileges and may modify any field.
        Otherwise only keys listed in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a field that is not present in the
        original record, or if a non‑admin attempts to modify a disallowed field.
    """
    # Make a shallow copy so the original record is not mutated
    updated_record = deepcopy(employee_record)

    for key, new_value in adjustments.items():
        if key not in employee_record:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")

        if not admin_flag and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users are not permitted to modify the field '{key}'."
            )

        updated_record[key] = new_value

    return updated_record