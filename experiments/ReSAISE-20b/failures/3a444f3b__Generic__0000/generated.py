# -*- coding: utf-8 -*-
"""
Utility module for editing personnel records with access control.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"position", "department"}


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee record after applying valid adjustments.

    Parameters
    ----------
    employee_record : dict
        The current state of the employee's details.
    adjustments : dict
        Mapping of field names to new values that should be applied.
    admin_flag : bool
        If True, the caller has administrative privileges and can modify any field.

    Returns
    -------
    dict
        A new dictionary representing the employee record after changes.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a field that the caller is not allowed to edit,
        or if the adjustment references a non‑existent key in ``employee_record``.
    """
    # Make a shallow copy to avoid mutating the input dictionary.
    updated_record = deepcopy(employee_record)

    for field, new_value in adjustments.items():
        # Ensure the field exists on the employee record.
        if field not in updated_record:
            raise ValueError(f"Field '{field}' does not exist in the employee record.")

        # Check permissions.
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change.
        updated_record[field] = new_value

    return updated_record