#!/usr/bin/env python3
"""
Secure employee record editor.

The module provides a single public function, `edit_personnel_info`, that
applies updates to an employee record while enforcing strict attribute
whitelisting.  Non‑admin users are limited to a predefined set of editable
fields, and sensitive fields (e.g. `social_security_number`) can only be
modified by an administrator.

The implementation follows best practices for security:
* Defensive copying of input data to avoid accidental mutation.
* Explicit validation of field names against a whitelist.
* No dynamic attribute resolution – all keys are checked statically.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global whitelist of fields that may be edited by non‑admin users.
# Add or remove field names here to control access.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is intentionally omitted; only admins may change it.
}

# --------------------------------------------------------------------------- #
def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Apply a set of updates to an employee record while enforcing
    access controls.

    Parameters
    ----------
    employee_record : dict
        The current state of the employee's details.  It is **not**
        modified in place; a new dictionary is returned.
    adjustments : dict
        Key‑value pairs representing the desired changes.
    admin_flag : bool
        ``True`` if the caller has administrative privileges,
        otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a field that is not present
        in the original record, or if a non‑admin tries to edit a field
        outside `EDITABLE_FIELDS`.

    Notes
    -----
    * Unknown fields in ``adjustments`` are ignored to avoid accidental
      injection of new keys.
    * The function performs a shallow copy; nested mutable objects are
      shared between the original and updated records.  If deep isolation
      is required, replace `copy.copy` with `copy.deepcopy`.
    """
    # Defensive copy of the original record to avoid side effects.
    updated = copy.copy(employee_record)

    for key, new_value in adjustments.items():
        # Skip unknown keys – they are ignored to avoid uncontrolled changes.
        if key not in employee_record:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")

        # Enforce access control for non‑admin users.
        if not admin_flag and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users are not permitted to modify the field '{key}'."
            )

        # Apply the change.
        updated[key] = new_value

    return updated