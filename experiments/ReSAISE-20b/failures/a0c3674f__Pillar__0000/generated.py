# -*- coding: utf-8 -*-
"""
Employee record modification module.

This module provides a single public function, `modify_staff_info`, that
creates an updated copy of an employee record dictionary based on a set of
requested changes.  The function enforces access control: only users with
admin privileges may modify fields that are not listed in the global
`EDITABLE_FIELDS`.  The function is defensive against accidental mutation of
the original record and checks that every change refers to a valid field.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by making sure that the returned dictionary is a fresh copy and that no
external resources (e.g., files or database connections) are leaked.
"""

from __future__ import annotations

# Fields that non‑admin users may edit.  All other fields require admin rights.
EDITABLE_FIELDS = {"name", "position", "department"}

# Sensitive field that must never be edited by non‑admin users.
SENSITIVE_FIELDS = {"social_security_number", "salary"}


def modify_staff_info(
    staff: dict,
    changes: dict,
    admin_status: bool,
) -> dict:
    """
    Return a new employee record with the requested changes applied.

    Parameters
    ----------
    staff : dict
        Current state of the employee record.  Expected keys include:
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    changes : dict
        Mapping of field names to new values that should be applied.
    admin_status : bool
        ``True`` if the caller has administrative privileges, otherwise
        ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a requested change references an unknown field or a non‑admin user
        attempts to modify a restricted field.
    """
    # Ensure the original record is not mutated by creating a shallow copy
    updated = staff.copy()

    # Validate each requested change
    for field, new_value in changes.items():
        if field not in staff:
            raise ValueError(f"Unknown field '{field}' cannot be updated.")

        if not admin_status:
            # Non‑admin users may only change fields listed in EDITABLE_FIELDS
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify the field '{field}'."
                )
            # Explicitly disallow modifications to sensitive fields
            if field in SENSITIVE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify the sensitive field '{field}'."
                )

        # Apply the change
        updated[field] = new_value

    return updated


# Example usage (for manual testing only; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    staff_record = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Admin modifies salary
    new_record = modify_staff_info(
        staff=staff_record,
        changes={"salary": 90000},
        admin_status=True,
    )
    print("Admin updated record:", new_record)

    # Non-admin attempts to change department
    try:
        modify_staff_info(
            staff=staff_record,
            changes={"department": "Marketing"},
            admin_status=False,
        )
    except ValueError as exc:
        print("Non‑admin error:", exc)