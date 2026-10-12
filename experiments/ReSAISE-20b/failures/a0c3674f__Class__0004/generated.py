#!/usr/bin/env python3
"""
Utility module for updating employee records safely.

The global `EDITABLE_FIELDS` defines the only fields a non‑admin user
is allowed to modify.  Any attempt by a non‑admin to change a protected
field results in a `PermissionError`.  Admin users may modify any field.

This module deliberately avoids using any form of dynamic code execution
to mitigate CWE‑913 (Improper Control of Dynamically‑Managed Code Resources).
"""

from __future__ import annotations
import copy
from typing import Dict, Any

# Fields that a non‑admin user may edit.  All other fields are considered
# protected and can only be modified by an admin.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return an updated copy of the employee record after applying valid changes.

    Parameters
    ----------
    staff : dict
        Current state of the employee's details.
    changes : dict
        Desired modifications.  Keys are field names, values are new data.
    admin_status : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a protected field.
    ValueError
        If ``changes`` contains keys that are not present in the original record
        and the caller is not an admin.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_staff = copy.deepcopy(staff)

    for field, new_value in changes.items():
        # Ensure the field exists in the original record
        if field not in staff:
            if admin_status:
                # Admins can add new fields
                updated_staff[field] = new_value
                continue
            else:
                raise ValueError(f"Field '{field}' does not exist in the staff record.")

        # Non‑admin users may only modify editable fields
        if not admin_status and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 75000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change salary (allowed) and SSN (not allowed)
    try:
        changes = {"salary": 80000, "social_security_number": "987-65-4321"}
        updated = modify_staff_info(employee, changes, admin_status=False)
    except Exception as e:
        print(f"Error: {e}")

    # Admin updating SSN
    updated = modify_staff_info(employee, {"social_security_number": "987-65-4321"}, admin_status=True)
    print(updated)