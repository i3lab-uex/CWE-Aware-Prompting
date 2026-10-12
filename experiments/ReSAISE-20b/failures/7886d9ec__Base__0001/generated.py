#!/usr/bin/env python3
"""
Utility to safely adjust employee profile data.

The module defines a global constant `EDITABLE_FIELDS` which lists the
dictionary keys that can be modified by non‑admin users.  The function
`adjust_employee_details` applies a set of alterations to an employee
profile while enforcing this restriction.  If a non‑admin attempts to
modify a protected field, a `ValueError` is raised.

CWE-915 (Improperly Controlled Modification of Dynamically‑Determined
Object Attributes) is mitigated by explicit whitelisting of allowed
attributes.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Keys that may be modified by non‑admin users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add any other fields that are considered safe for general editing.
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: dict,
    alterations: dict,
    has_admin_rights: bool = False
) -> dict:
    """
    Return a new employee profile dictionary with requested alterations applied.

    Parameters
    ----------
    person : dict
        Current employee profile.
    alterations : dict
        Keys and values to be updated in the profile.
    has_admin_rights : bool, default False
        If ``True``, all alterations are applied.  Non‑admin users may only
        modify keys listed in :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a field not in
        :data:`EDITABLE_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of ``person``; nested objects are not
    deeply copied.  The caller should be aware that any mutable sub‑objects
    shared between the original and returned dictionaries may still be
    modified in place.
    """
    # Create a shallow copy to avoid mutating the original profile
    updated_profile = person.copy()

    # Determine which keys are allowed to be altered
    if has_admin_rights:
        allowed_keys = set(alterations.keys())
    else:
        # Non‑admin: only allow keys that are explicitly editable
        allowed_keys = set(alterations.keys()) & EDITABLE_FIELDS

    # Identify any disallowed keys
    disallowed = set(alterations.keys()) - allowed_keys
    if disallowed:
        raise ValueError(
            f"Non‑admin user attempted to modify protected fields: "
            f"{', '.join(sorted(disallowed))}"
        )

    # Apply the allowed alterations
    for key in allowed_keys:
        updated_profile[key] = alterations[key]

    return updated_profile

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempting to change salary (should fail)
    try:
        adjust_employee_details(
            employee,
            {"salary": 95000},
            has_admin_rights=False
        )
    except ValueError as exc:
        print(f"Caught expected error: {exc}")

    # Admin updating salary and SSN
    updated = adjust_employee_details(
        employee,
        {"salary": 95000, "social_security_number": "987-65-4321"},
        has_admin_rights=True
    )
    print("Updated profile:", updated)