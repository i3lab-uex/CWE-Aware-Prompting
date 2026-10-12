#!/usr/bin/env python3
"""
Secure staff record modification module.

This module provides the function `modify_staff_info` that safely updates
employee records while preventing unauthorized or accidental changes to
protected attributes. It follows the principle of least privilege and
protects against CWE‑915: Improperly Controlled Modification of Dynamically-
Determined Object Attributes.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List


# --------------------------------------------------------------------------- #
# Global configuration: fields that a non‑admin user may edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: List[str] = [
    "name",
    "position",
    "salary",
    "department",
]

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class UnauthorizedFieldModificationError(ValueError):
    """Raised when a user attempts to modify a protected field."""


class InvalidFieldError(ValueError):
    """Raised when the requested change refers to a non‑existent field."""


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return an updated staff dictionary after applying valid changes.

    Parameters
    ----------
    staff : dict
        Current employee record. Keys are attribute names.
    changes : dict
        Desired updates: key -> new value.
    admin_status : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated record.

    Raises
    ------
    UnauthorizedFieldModificationError
        If a non‑admin attempts to modify a protected field.
    InvalidFieldError
        If any key in `changes` does not exist in the staff record.
    """
    # Make a deep copy to avoid mutating the original dictionary
    updated_staff = copy.deepcopy(staff)

    for field, new_value in changes.items():
        # Validate that the field exists
        if field not in staff:
            raise InvalidFieldError(f"Attempted to modify non‑existent field '{field}'.")

        # Enforce privilege restrictions
        if not admin_status and field not in EDITABLE_FIELDS:
            raise UnauthorizedFieldModificationError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_staff = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin updates
    admin_changes = {"salary": 90000, "social_security_number": "987-65-4321"}
    print(modify_staff_info(sample_staff, admin_changes, True))

    # Non‑admin attempts a protected change
    try:
        non_admin_changes = {"social_security_number": "111-22-3333"}
        modify_staff_info(sample_staff, non_admin_changes, False)
    except Exception as e:
        print(f"Error: {e}")