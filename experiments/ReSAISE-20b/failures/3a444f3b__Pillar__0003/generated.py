#!/usr/bin/env python3
"""
Edit employee records with role‑based field restrictions.

The module defines a single public function:
    edit_personnel_info(employee_record, adjustments, admin_flag)

The function safely updates an employee dictionary in place only for
fields that are permitted by the caller's role. It performs deep copies to
avoid accidental mutation of shared data structures and validates that
only existing keys are modified.

Security Considerations:
    * Non‑admin users can modify only the fields listed in
      EDITABLE_FIELDS.
    * Admin users may modify any field present in the record.
    * The function raises ValueError for attempts to modify non‑existent
      keys or forbidden fields.
    * A shallow copy of the employee record is returned to avoid side
      effects on external references.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def _validate_field(field: str, record_keys: set[str]) -> None:
    """
    Ensure the field exists in the employee record.
    Raise ValueError if it does not.
    """
    if field not in record_keys:
        raise ValueError(f"Field '{field}' does not exist in the employee record.")

def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool
) -> Dict[str, Any]:
    """
    Return an updated employee record dictionary after applying allowed adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key-value pairs for fields and their new data.
    admin_flag : bool
        True if the updater is an administrator.

    Returns
    -------
    dict
        A new dictionary reflecting the valid changes.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a non‑existent field or a
        forbidden field for non‑admin users.
    """
    # Work on a shallow copy to preserve the original record
    updated_record = copy.deepcopy(employee_record)

    # Pre‑compute existing keys for validation
    record_keys = set(updated_record.keys())

    for field, new_value in adjustments.items():
        # Validate that the field exists
        _validate_field(field, record_keys)

        if not admin_flag:
            # Non‑admin users can only modify EDITABLE_FIELDS
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify field '{field}'."
                )

        # Apply the change
        updated_record[field] = new_value

    return updated_record