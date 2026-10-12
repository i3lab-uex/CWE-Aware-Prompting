#!/usr/bin/env python3
"""
Employee data modification utility.

The module defines a single public function, `modify_employee_data`, that
updates an employee dictionary with a set of proposed alterations.  
If the caller does not have administrative privileges, only fields
listed in `EDITABLE_FIELDS` are allowed to be modified.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class UnauthorizedFieldModification(ValueError):
    """
    Raised when a caller attempts to modify a field they are not allowed to.
    """


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_inputs(worker: dict, alterations: dict) -> None:
    """
    Basic validation of the inputs.

    Parameters
    ----------
    worker : dict
        The original employee record.
    alterations : dict
        Proposed changes to apply.

    Raises
    ------
    TypeError
        If either argument is not a mapping.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool = False
) -> dict:
    """
    Update an employee record with the supplied alterations.

    Parameters
    ----------
    worker : dict
        The original employee data.
    alterations : dict
        Keys are field names, values are the new values to assign.
    admin_privileges : bool
        If ``True`` all fields may be updated.  Otherwise only the keys
        listed in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The input
        ``worker`` is not modified.

    Raises
    ------
    UnauthorizedFieldModification
        If a non‑admin attempts to change a field not in
        :data:`EDITABLE_FIELDS`.
    TypeError
        If the inputs are not dictionaries.
    """
    _validate_inputs(worker, alterations)

    # Make a shallow copy to avoid mutating the original record.
    updated_worker = worker.copy()

    for field, new_value in alterations.items():
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise UnauthorizedFieldModification(
                f"Non‑admin users cannot modify the field '{field}'."
            )
        updated_worker[field] = new_value

    return updated_worker


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_worker = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    changes = {
        "salary": 90000,
        "department": "Research & Development"
    }

    # Admin can change any field
    print(modify_employee_data(sample_worker, changes, admin_privileges=True))

    # Regular user: will raise an exception because 'salary' is not editable
    try:
        print(modify_employee_data(sample_worker, changes))
    except UnauthorizedFieldModification as exc:
        print(f"Error: {exc}")