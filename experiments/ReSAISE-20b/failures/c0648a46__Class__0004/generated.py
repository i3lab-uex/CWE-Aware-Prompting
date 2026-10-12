#!/usr/bin/env python3
"""
Employee profile updater.

This module provides a single function, `modify_employee_profile`, which updates an
employee's profile dictionary based on supplied changes while respecting the
permissions of the caller.

Security note:
- Only fields listed in `EDITABLE_FIELDS` may be updated by non‑privileged users.
- Privileged (admin) callers can modify any field present in the profile.
- The function never evaluates arbitrary code or executes dynamic content.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add more fields as needed
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_employee_profile(
    worker: dict,
    changes: dict,
    is_privileged: bool
) -> dict:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker : dict
        Current employee profile. Must be a mapping of field names to values.
    changes : dict
        Desired updates. Keys are field names, values are the new data to store.
    is_privileged : bool
        If True, all fields in `changes` are applied. If False,
        only fields listed in `EDITABLE_FIELDS` are updated.

    Returns
    -------
    dict
        A new dictionary containing the merged profile data. The original
        `worker` dict is left untouched.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify a field not in
        `EDITABLE_FIELDS`.
    TypeError
        If any argument is of an unexpected type.
    """

    # Input validation
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")
    if not isinstance(is_privileged, bool):
        raise TypeError("is_privileged must be a boolean")

    # Create a shallow copy to avoid mutating the original worker dict
    updated_profile = worker.copy()

    # Process each change request
    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise TypeError(f"Field name must be a string, got {type(field).__name__}")

        # Non‑privileged check
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: non‑privileged users cannot modify '{field}'"
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_worker = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789"
    }

    changes_to_apply = {
        "salary": 90000,          # Only admin can change
        "department": "Product",  # Allowed for non‑admin
    }

    try:
        updated = modify_employee_profile(sample_worker, changes_to_apply, is_privileged=False)
        print("Updated profile:", updated)
    except Exception as e:
        print("Error:", e)