#!/usr/bin/env python3
"""
Utility to safely modify employee records.

The function enforces field-level permissions and protects sensitive data.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users may edit.
EDITABLE_FIELDS = {"name", "position", "department"}

# Sensitive fields that require admin privileges.
SENSITIVE_FIELDS = {"salary", "social_security_number"}


def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool
) -> Dict[str, Any]:
    """
    Return a new staff dictionary with the requested changes applied.

    Parameters
    ----------
    staff : dict
        Current employee record.
    changes : dict
        Desired field updates (key: new value).
    admin_status : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field, or if the change
        contains keys that are not part of the staff record.
    """
    # Create a shallow copy to avoid mutating the original dict
    updated_staff = deepcopy(staff)

    for field, new_value in changes.items():
        # Reject unknown fields
        if field not in staff:
            raise ValueError(f"Field '{field}' does not exist in the staff record.")

        # Enforce permissions
        if field in SENSITIVE_FIELDS and not admin_status:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Non‑admins are only allowed to change EDITABLE_FIELDS
        if not admin_status and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff