#!/usr/bin/env python3
"""
Employee profile modification utility.

This module defines a single function, `modify_employee_profile`, which safely updates
an employee profile dictionary.  It enforces an attribute whitelist to prevent
uncontrolled modifications of sensitive fields (CWE‑915).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of fields that non‑admin users may modify
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Non‑admin users may update contact information but not compensation
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class ProfileModificationError(RuntimeError):
    """Base exception for profile modification errors."""


class UnauthorizedFieldChange(ProfileModificationError):
    """Raised when a user attempts to modify a non‑editable field."""


class InvalidProfile(ProfileModificationError):
    """Raised when the provided profile is not a dictionary or missing required keys."""


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def modify_employee_profile(
    worker: dict,
    changes: dict,
    is_privileged: bool = False
) -> dict:
    """
    Safely modify an employee profile dictionary.

    Parameters
    ----------
    worker : dict
        The current employee profile. Must be a dictionary containing the keys
        expected in an employee record (e.g., name, position, salary, etc.).
    changes : dict
        A mapping of fields to new values that should be applied to the profile.
    is_privileged : bool, default False
        Indicates whether the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile. The original
        `worker` dictionary is not mutated.

    Raises
    ------
    InvalidProfile
        If `worker` is not a dictionary or lacks essential keys.
    UnauthorizedFieldChange
        If a non‑privileged user attempts to modify a field not in EDITABLE_FIELDS.
    """
    if not isinstance(worker, dict):
        raise InvalidProfile("Worker profile must be a dictionary.")

    # Make a shallow copy to avoid mutating the original
    updated_profile = worker.copy()

    for field, new_value in changes.items():
        # 1. Ensure the field exists in the profile
        if field not in worker:
            raise InvalidProfile(f"Field '{field}' does not exist in the profile.")

        # 2. Enforce access control
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise UnauthorizedFieldChange(
                f"Modification of '{field}' is not allowed for non‑privileged users."
            )

        # 3. Apply the change
        updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_profile = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change salary (should raise)
    try:
        modify_employee_profile(
            worker=sample_profile,
            changes={"salary": 90000},
            is_privileged=False
        )
    except UnauthorizedFieldChange as e:
        print(f"Unauthorized change detected: {e}")

    # Admin changing salary (allowed)
    updated = modify_employee_profile(
        worker=sample_profile,
        changes={"salary": 90000},
        is_privileged=True
    )
    print("Updated profile:", updated)