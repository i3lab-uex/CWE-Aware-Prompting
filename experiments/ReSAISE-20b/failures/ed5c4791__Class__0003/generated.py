#!/usr/bin/env python3
"""
Employee data modification module.

This module provides a single public function, `modify_employee_data`,
which safely updates an employee record while enforcing field-level
permissions.  It protects against CWE‑913 by ensuring that only the
explicitly allowed attributes are changed and that no new attributes can
be injected by a non‑admin user.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Global configuration
# --------------------------------------------------------------------------- #

# Fields that any user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

# Fields that require admin privileges to modify.
ADMIN_ONLY_FIELDS = {"salary", "social_security_number"}

# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #

def _is_valid_key(key: str) -> bool:
    """
    Determine whether a key is considered valid for an employee record.
    Valid keys are those that exist in the base employee schema or are
    explicitly editable by an admin.
    """
    allowed_keys = (
        {"name", "position", "salary", "department", "social_security_number"}
    )
    return key in allowed_keys


def _validate_value(key: str, value) -> None:
    """
    Perform minimal type validation for each field.
    Raises a ValueError if the value is of an unexpected type.
    """
    type_map = {
        "name": str,
        "position": str,
        "department": str,
        "salary": (int, float),
        "social_security_number": str,
    }

    expected_type = type_map.get(key)
    if expected_type is None:
        # Unknown key; let the caller handle it.
        return

    if not isinstance(value, expected_type):
        raise ValueError(
            f"Invalid type for field '{key}': "
            f"expected {expected_type}, got {type(value)}"
        )


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool = False,
) -> dict:
    """
    Safely update an employee's record.

    Parameters
    ----------
    worker : dict
        The original employee record.  Must contain at least the keys:
        'name', 'position', 'salary', 'department', and
        'social_security_number'.
    alterations : dict
        Proposed changes keyed by attribute name.
    admin_privileges : bool, optional
        If True, the caller has administrative rights and can modify any
        field.  Defaults to False.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If an alteration attempts to modify a non‑existent field.
    PermissionError
        If a regular user tries to alter an admin‑only field.
    ValueError
        If a provided value does not match the expected type for its key.

    Notes
    -----
    - The function returns a new dictionary; the original `worker` is left
      untouched.
    - Only keys present in the base employee schema may be altered.
    """
    # Ensure we are not mutating the original dictionary
    updated = worker.copy()

    for key, new_value in alterations.items():
        # Reject unknown keys outright
        if not _is_valid_key(key):
            raise KeyError(f"Attempted to modify unknown field '{key}'")

        # Check permissions
        if not admin_privileges:
            if key in ADMIN_ONLY_FIELDS:
                raise PermissionError(
                    f"Insufficient privileges to modify field '{key}'"
                )
            if key not in EDITABLE_FIELDS:
                raise PermissionError(
                    f"Field '{key}' is not editable by regular users"
                )

        # Validate value type
        _validate_value(key, new_value)

        # Apply the change
        updated[key] = new_value

    return updated


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_worker = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Regular user attempts to change name and salary
    try:
        result = modify_employee_data(
            sample_worker,
            {"name": "Jane Smith", "salary": 90000},
            admin_privileges=False,
        )
    except Exception as e:
        print(f"Regular user error: {e}")

    # Admin user changes salary
    try:
        result = modify_employee_data(
            sample_worker,
            {"salary": 90000},
            admin_privileges=True,
        )
        print("Admin update successful:", result)
    except Exception as e:
        print(f"Admin error: {e}")