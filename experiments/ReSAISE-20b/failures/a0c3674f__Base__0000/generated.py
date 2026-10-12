# -*- coding: utf-8 -*-
"""
Employee record modification utility.

This module defines a single public function, :func:`modify_staff_info`,
which safely applies updates to an employee record dictionary.  The
function enforces that only a whitelisted set of fields may be updated by
non‑admin users, mitigating CWE-915: Improperly Controlled Modification of
Dynamically‑Determined Object Attributes.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that are safe to modify by non‑admin users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is editable only for admins; included here to allow admins.
    "salary",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_staff_info(
    staff: dict,
    changes: dict,
    admin_status: bool
) -> dict:
    """
    Apply a set of changes to an employee record.

    Parameters
    ----------
    staff : dict
        The original employee dictionary.  Keys may include:
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number`` among others.
    changes : dict
        Proposed updates.  Keys are field names and values are the new data.
    admin_status : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated record.  The original
        ``staff`` dictionary is never modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a disallowed field, or if the
        ``changes`` dictionary contains keys that are not valid employee
        attributes.

    Notes
    -----
    * The function performs a shallow copy of the input dictionary; nested
      mutable objects are not deep‑cloned.
    * Keys that start with ``__`` or contain a dot (.) are rejected to
      prevent accidental modification of Python internals or nested keys.
    * The function does not validate the data type of new values; callers
      should perform additional validation if necessary.
    """
    # Defensive copy to avoid mutating the caller's data
    updated = dict(staff)

    # Valid keys are those present in the original staff dictionary.
    valid_keys = set(staff.keys())

    # Reject keys that look like special attributes or nested paths.
    forbidden_prefixes = ("__",)
    for key in changes:
        if any(key.startswith(prefix) for prefix in forbidden_prefixes):
            raise ValueError(f"Modification of internal attribute '{key}' is not allowed.")
        if "." in key:
            raise ValueError(f"Nested attribute '{key}' is not supported.")
        if key not in valid_keys:
            raise ValueError(f"Field '{key}' does not exist in the staff record.")

        # Non‑admin users may only modify fields listed in EDITABLE_FIELDS
        if not admin_status and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify field '{key}'. "
                "Only the following fields are editable: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        # Apply the change
        updated[key] = changes[key]

    return updated

# --------------------------------------------------------------------------- #
# Example usage (commented out; remove comments to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    staff_record = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Admin updating salary
    changes_admin = {"salary": 90000}
    updated_staff = modify_staff_info(staff_record, changes_admin, admin_status=True)
    print(updated_staff)

    # Non-admin attempting to change SSN (should raise ValueError)
    changes_user = {"social_security_number": "987-65-4321"}
    try:
        modify_staff_info(staff_record, changes_user, admin_status=False)
    except ValueError as exc:
        print(f"Error: {exc}")