# -*- coding: utf-8 -*-
"""
Utility module for staff record modifications.

The module defines a global list `EDITABLE_FIELDS` which contains the
attribute names that can be changed by non‑admin users.  The function
`modify_staff_info` performs a safe, limited update of an employee record.
"""

from __future__ import annotations

# Global list of fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = ["name", "position", "salary", "department"]


def modify_staff_info(
    staff: dict,
    changes: dict,
    admin_status: bool
) -> dict:
    """
    Return an updated copy of *staff* with the provided *changes* applied.

    Parameters
    ----------
    staff : dict
        Current employee record.  Keys are expected to be strings.
    changes : dict
        Desired updates, mapping field names to new values.
    admin_status : bool
        If ``True`` the caller is an administrator and may modify any field.
        If ``False`` only fields listed in :data:`EDITABLE_FIELDS` may be
        modified.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        * If a key in ``changes`` does not exist in ``staff``.
        * If a non‑admin attempts to modify a field that is not editable.
    TypeError
        If *staff* or *changes* are not dictionaries.

    Notes
    -----
    The function does **not** modify the original ``staff`` dictionary; it
    returns a new instance.  This avoids accidental side effects and makes
    the function safe to use in concurrent contexts.
    """
    # Basic type checks
    if not isinstance(staff, dict):
        raise TypeError("`staff` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated = staff.copy()

    for key, new_value in changes.items():
        # Ensure the field exists on the record
        if key not in staff:
            raise ValueError(f"Field '{key}' does not exist on the staff record")

        # Enforce editable restrictions for non‑admins
        if not admin_status and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'"
            )

        # Apply the change
        updated[key] = new_value

    return updated


# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     employee = {
#         "name": "Alice",
#         "position": "Engineer",
#         "salary": 70000,
#         "department": "R&D",
#         "social_security_number": "123-45-6789"
#     }
#
#     # Admin updates everything
#     print(modify_staff_info(employee, {"salary": 75000, "department": "Product"}, True))
#
#     # Non-admin attempts to change salary (not allowed)
#     try:
#         print(modify_staff_info(employee, {"salary": 75000}, False))
#     except ValueError as e:
#         print(e)