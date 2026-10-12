#!/usr/bin/env python3
"""
Employee profile modification utility.

The module defines a single public function `modify_employee_profile` that updates
the fields of an employee profile dictionary in a controlled and secure manner.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: fields that a non‑admin user may edit
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other safe fields as needed
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile dictionary with the supplied changes.

    Parameters
    ----------
    worker : dict
        The original employee profile.
    changes : dict
        Mapping of field names to new values. Only keys that are present in
        ``EDITABLE_FIELDS`` may be applied unless the caller is privileged.
    is_privileged : bool
        If ``True`` the caller has administrative privileges and may modify any
        field.  Non‑privileged callers are restricted to the fields listed in
        ``EDITABLE_FIELDS``.

    Returns
    -------
    dict
        A new dictionary containing the updated profile. The original ``worker``
        object is left untouched.

    Raises
    ------
    TypeError
        If ``worker`` or ``changes`` is not a dictionary.
    ValueError
        If a non‑privileged caller attempts to modify a disallowed field.

    Notes
    -----
    * The function performs a shallow copy of ``worker`` before applying changes.
      This protects the caller from accidental side‑effects.
    * Sensitive fields such as ``social_security_number`` are never modifiable
      by non‑privileged users because they are not included in ``EDITABLE_FIELDS``.
    * The function does **not** perform type validation on the new values; callers
      should ensure that values are of the expected types for each field.
    """
    # Input validation
    if not isinstance(worker, dict):
        raise TypeError(f"'worker' must be a dict; got {type(worker).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dict; got {type(changes).__name__}")

    # Create a shallow copy to avoid mutating the original
    updated_profile = copy.copy(worker)

    for field, new_value in changes.items():
        # Ensure the key is a string to avoid accidental attribute injection
        if not isinstance(field, str):
            raise TypeError(f"Field names must be strings; got {type(field).__name__}")

        # Non‑privileged users are limited to EDITABLE_FIELDS
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' is not editable for non‑privileged users."
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only; remove or guard under __main__)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Developer", "salary": 95000}

    # Non‑privileged attempt: should raise ValueError
    try:
        modify_employee_profile(employee, changes, is_privileged=False)
    except ValueError as exc:
        print(f"Non‑privileged error: {exc}")

    # Privileged update
    updated = modify_employee_profile(employee, changes, is_privileged=True)
    print("Updated profile:", updated)