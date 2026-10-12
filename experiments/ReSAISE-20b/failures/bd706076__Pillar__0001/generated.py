# -*- coding: utf-8 -*-
"""
Utility for updating employee records with proper access control.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool
) -> Dict[str, Any]:
    """
    Update an employee record.

    Parameters
    ----------
    employee : dict
        Original employee data. Keys may include:
        'name', 'position', 'salary', 'department',
        'social_security_number'.
    updates : dict
        Fields to be updated with their new values.
    is_admin : bool
        Flag indicating whether the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.
        The original ``employee`` object is left untouched.

    Raises
    ------
    KeyError
        If an update refers to a field that does not exist in ``employee``.
    PermissionError
        If a non‑admin attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    ValueError
        If ``updates`` is empty or not a mapping.

    Notes
    -----
    * The function performs shallow validation of the update payload.
      It does not perform type checks or deep validation of field values.
    * This implementation mitigates CWE‑664 by ensuring that the
      original employee record is never mutated; a new dictionary
      is created and returned.
    """
    if not isinstance(updates, dict):
        raise ValueError("updates must be a mapping type")
    if not updates:
        # No-op: simply return a copy of the original record
        return deepcopy(employee)

    # Create a shallow copy to avoid side effects on the caller's dict
    updated = deepcopy(employee)

    for field, new_value in updates.items():
        if field not in employee:
            raise KeyError(f"Field '{field}' does not exist on the employee record")

        if not is_admin and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'"
            )

        updated[field] = new_value

    return updated