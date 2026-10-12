#!/usr/bin/env python3
"""
Employee profile adjustment module.

Provides a single public function `adjust_employee_profile` that updates an employee's
dictionary while enforcing edit permissions based on user role.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

#: Fields that a regular user may modify.  Admins can edit any field.
EDITABLE_FIELDS = {"name", "position", "department"}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _validate_inputs(emp: dict, changes: dict) -> None:
    """
    Validate the types of the arguments.

    Raises
    ------
    TypeError
        If `emp` or `changes` is not a dictionary.
    """
    if not isinstance(emp, dict):
        raise TypeError(f"emp must be a dict; got {type(emp).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict; got {type(changes).__name__}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def adjust_employee_profile(emp: dict, changes: dict, has_admin_rights: bool) -> dict:
    """
    Update an employee's profile with the given changes.

    Parameters
    ----------
    emp : dict
        The original employee dictionary.  Must contain keys such as
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    changes : dict
        A mapping of attribute names to the new values that should be applied.
    has_admin_rights : bool
        ``True`` if the caller is an administrator and may edit any field.
        ``False`` restricts edits to :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        The updated employee dictionary.  The original ``emp`` is **not**
        modified; a new dictionary is returned.

    Raises
    ------
    TypeError
        If ``emp`` or ``changes`` is not a dictionary.
    ValueError
        If a non‑admin attempts to modify a field outside of
        :data:`EDITABLE_FIELDS`.
    """
    # Validate inputs first.
    _validate_inputs(emp, changes)

    # Create a shallow copy so the original dict remains untouched.
    updated_emp = emp.copy()

    for key, value in changes.items():
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify field '{key}'. "
                f"Editable fields: {sorted(EDITABLE_FIELDS)}"
            )
        # Optionally, we could add type checks or sanitization here.
        updated_emp[key] = value

    return updated_emp


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee data
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin attempting to change salary
    admin_changes = {"salary": 90000}
    print(
        adjust_employee_profile(employee, admin_changes, has_admin_rights=True)
    )

    # Regular user attempting to change salary (should raise ValueError)
    try:
        adjust_employee_profile(employee, admin_changes, has_admin_rights=False)
    except ValueError as exc:
        print(f"Permission error: {exc}")