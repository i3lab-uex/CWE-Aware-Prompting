#!/usr/bin/env python3
"""
Employee record updater with security checks.

This module defines a single public function, ``update_employee_record``, which
updates an employee dictionary safely.  It prevents regular users from changing
protected fields (e.g., ``social_security_number``) by limiting the set of
modifiable attributes to those defined in ``EDITABLE_FIELDS``.  Admin users are
allowed to modify any existing field.

The implementation follows the guidelines for CWE‑915 by ensuring that only
whitelisted attributes are updated and that no arbitrary attribute injection is
possible.
"""

from __future__ import annotations

from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "salary",
    "department",
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Update an employee record safely.

    Parameters
    ----------
    employee : dict
        The original employee data.  Must contain string keys.
    updates : dict
        A mapping of fields to new values.
    is_admin : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    TypeError
        If ``employee`` or ``updates`` is not a mapping.
    ValueError
        If an attempt is made to modify a protected field or a non‑existent
        attribute.
    """
    # Basic type checks
    if not isinstance(employee, dict):
        raise TypeError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Create a shallow copy to avoid mutating the caller's data
    updated = employee.copy()

    # Determine which fields are allowed to be modified
    if is_admin:
        allowed_fields = set(employee.keys())
    else:
        # Regular users can only modify the defined editable fields
        allowed_fields = EDITABLE_FIELDS & set(employee.keys())

    for field, new_value in updates.items():
        # Reject attempts to modify non‑existent attributes
        if field not in employee:
            raise ValueError(f"Field '{field}' does not exist on the employee record")

        # Reject attempts to modify protected fields unless admin
        if field not in allowed_fields:
            raise ValueError(
                f"Field '{field}' cannot be modified by a non‑admin user"
            )

        # Apply the update
        updated[field] = new_value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee record
    emp = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 75000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Regular user attempting to change salary and SSN
    try:
        print(
            update_employee_record(
                emp,
                {"salary": 80000, "social_security_number": "987-65-4321"},
                is_admin=False,
            )
        )
    except ValueError as exc:
        print(f"Regular user error: {exc}")

    # Admin updating all fields
    updated_emp = update_employee_record(
        emp,
        {"salary": 80000, "social_security_number": "987-65-4321"},
        is_admin=True,
    )
    print("Admin updated record:", updated_emp)