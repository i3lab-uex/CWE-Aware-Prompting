# -*- coding: utf-8 -*-
"""
Employee data modification module.

This module provides a single public function `modify_employee_data` that
updates an employee dictionary with new values.  Regular users are only
allowed to modify a predefined set of fields, while administrators can
modify any field except those explicitly protected.

The implementation guards against accidental or malicious changes to
sensitive attributes (e.g., `social_security_number`) and protects the
function from unintended side‑effects by returning a new dictionary.
"""

from __future__ import annotations

# Fields that regular users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}

# Fields that should never be altered, even by admins
PROTECTED_FIELDS = {"social_security_number", "salary"}

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool
) -> dict:
    """
    Update an employee dictionary with the given alterations.

    Parameters
    ----------
    worker : dict
        The original employee record.  Keys are attribute names.
    alterations : dict
        Proposed changes, mapping attribute names to new values.
    admin_privileges : bool
        ``True`` if the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in ``EDITABLE_FIELDS``,
        or if any alteration targets a protected field.
    """
    # Create a copy to avoid mutating the input dictionary
    updated_worker = worker.copy()

    for field, new_value in alterations.items():
        # Check if the field is protected
        if field in PROTECTED_FIELDS:
            raise ValueError(
                f"Modification of protected field '{field}' is not allowed."
            )

        # Non‑admin users may only modify editable fields
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"User lacks permission to modify field '{field}'."
            )

        # Perform the update
        updated_worker[field] = new_value

    return updated_worker


# Example usage (for illustration; remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    changes = {"position": "Senior Developer", "department": "R&D"}

    try:
        new_employee = modify_employee_data(employee, changes, admin_privileges=False)
        print("Updated employee:", new_employee)
    except ValueError as e:
        print("Failed to update:", e)