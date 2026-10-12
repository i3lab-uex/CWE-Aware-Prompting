#!/usr/bin/env python3
"""
Employee profile adjustment module.

This module provides a single public function, ``adjust_employee_profile``, which
updates an employee dictionary in a safe and controlled manner.  It prevents
regular users from changing sensitive fields such as ``salary`` or
``social_security_number`` by enforcing a whitelist of editable keys.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

# Only these fields may be edited by non‑admin users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other non‑sensitive fields here
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_employee_profile(
    emp: dict,
    changes: dict,
    has_admin_rights: bool
) -> dict:
    """
    Update an employee dictionary with the supplied changes.

    Parameters
    ----------
    emp : dict
        The original employee record.  It must contain keys such as
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    changes : dict
        Proposed modifications keyed by the attribute name.  Only keys that
        exist in ``emp`` are allowed.
    has_admin_rights : bool
        If True, the caller is an administrator and may modify any field.
        Otherwise only fields listed in :data:`EDITABLE_FIELDS` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``emp`` is not mutated.

    Raises
    ------
    KeyError
        If a change refers to an attribute that does not exist in ``emp``.
    PermissionError
        If a non‑admin user attempts to modify a disallowed field.

    Notes
    -----
    The function is intentionally defensive: it checks that every key in
    ``changes`` exists in the original employee dictionary, and for regular
    users it further ensures that only whitelisted fields are updated.  This
    mitigates CWE‑915 – *Improperly Controlled Modification of Dynamically-
    Determined Object Attributes*.
    """
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Validate that all requested changes refer to existing keys
    for key in changes:
        if key not in emp:
            raise KeyError(f"Attempted to modify unknown field '{key}'")

    # For non‑admin users, restrict modifications to editable fields
    if not has_admin_rights:
        disallowed = [k for k in changes if k not in EDITABLE_FIELDS]
        if disallowed:
            raise PermissionError(
                f"Non‑admin users cannot modify fields: {', '.join(disallowed)}"
            )

    # Create a shallow copy to avoid mutating the original
    updated_emp = emp.copy()
    updated_emp.update(changes)
    return updated_emp

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Regular user attempts to change position (allowed)
    try:
        new_emp = adjust_employee_profile(
            employee,
            {"position": "Senior Developer"},
            has_admin_rights=False
        )
        print("Regular update succeeded:", new_emp)
    except Exception as e:
        print("Regular update failed:", e)

    # Regular user attempts to change salary (disallowed)
    try:
        adjust_employee_profile(
            employee,
            {"salary": 95000},
            has_admin_rights=False
        )
    except Exception as e:
        print("Disallowed update error:", e)

    # Admin user updates salary
    try:
        new_emp_admin = adjust_employee_profile(
            employee,
            {"salary": 95000},
            has_admin_rights=True
        )
        print("Admin update succeeded:", new_emp_admin)
    except Exception as e:
        print("Admin update failed:", e)