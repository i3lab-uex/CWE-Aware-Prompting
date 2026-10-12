# -*- coding: utf-8 -*-
"""
Employee profile modification module.

This module defines a single function `modify_employee_profile` which updates an
employee's profile dictionary according to the caller's privileges.  The set of
fields that a non‑admin user may modify is controlled by the global constant
`EDITABLE_FIELDS`.  The function performs defensive checks to avoid accidental
leakage of sensitive information and ensures that the original profile is not
modified in place.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Constants
# --------------------------------------------------------------------------- #

# The set of keys that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # NOTE: Salary and SSN are protected fields.
}

# --------------------------------------------------------------------------- #
#  Core function
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
        The current employee profile.  Keys may include:
            - name (str)
            - position (str)
            - salary (float)
            - department (str)
            - social_security_number (str)
        The dictionary may contain additional keys; these are preserved.
    changes : dict
        Mapping of field names to new values that should be applied to the profile.
    is_privileged : bool
        ``True`` if the caller has admin privileges and may modify any field.
        ``False`` restricts modifications to those listed in ``EDITABLE_FIELDS``.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a requested change attempts to modify a protected field without admin
        privileges, or if the provided ``worker`` is not a dictionary.
    TypeError
        If ``changes`` is not a mapping type.

    Notes
    -----
    The function performs a shallow copy of the original profile to avoid side
    effects.  Only keys present in ``worker`` are considered; attempts to add new
    fields are ignored, preserving data integrity.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary representing the employee profile")

    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary of field updates")

    # Create a shallow copy to avoid mutating the original input
    updated_profile = worker.copy()

    for field, new_value in changes.items():
        # Skip keys that do not exist in the original profile
        if field not in worker:
            continue

        # Enforce privilege checks
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify protected field '{field}'."
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile

# --------------------------------------------------------------------------- #
#  Example usage (for internal testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee profile
    profile = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000.0,
        "department": "R&D",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempting to change salary (should raise)
    try:
        modify_employee_profile(profile, {"salary": 90000}, is_privileged=False)
    except ValueError as e:
        print(f"Expected error: {e}")

    # Admin changing salary
    new_profile = modify_employee_profile(profile, {"salary": 90000}, is_privileged=True)
    print("Updated profile:", new_profile)