#!/usr/bin/env python3
"""
Employee profile updater with restricted field editing.

The module defines a global constant EDITABLE_FIELDS that lists the
attributes a non‑admin user is allowed to modify.  The function
`modify_employee_profile` applies the requested changes safely, ensuring
that only permitted fields are altered and that no unintended side‑effects
occur.

Security considerations:
* The function performs explicit checks on field names.
* It creates a shallow copy of the original profile to avoid mutating
  the caller's data.
* Any attempt to modify a non‑editable field (when `is_privileged` is
  False) or a nonexistent field raises a ValueError, preventing silent
  failures.
* The implementation does not execute or import code from the `changes`
  dictionary, mitigating CWE‑913 (Improper Control of Dynamically‑Managed
  Code Resources).
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes
    applied.

    Parameters
    ----------
    worker : dict
        The original employee profile.
    changes : dict
        Mapping of field names to new values.
    is_privileged : bool
        If True, the caller has administrative privileges and may modify
        any field.  Otherwise only fields in EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a requested field does not exist in the profile or if a non‑admin
        tries to modify an uneditable field.
    """
    # Validate input types
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original profile
    updated_profile = copy.deepcopy(worker)

    for field, new_value in changes.items():
        if field not in worker:
            raise ValueError(f"Field '{field}' does not exist in the employee profile")

        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑privileged users cannot modify the field '{field}'"
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile


# Example usage (uncomment to test)
if __name__ == "__main__":
    original = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Developer", "salary": 100000}
    print("Non‑admin attempt:")
    try:
        new_profile = modify_employee_profile(original, changes, is_privileged=False)
        print(new_profile)
    except ValueError as e:
        print(f"Error: {e}")

    print("\nAdmin attempt:")
    new_profile = modify_employee_profile(original, changes, is_privileged=True)
    print(new_profile)