# -*- coding: utf-8 -*-

"""
Employee profile adjustment module.

The function ``adjust_employee_details`` updates an employee profile
dictionary with the provided alterations.  Non‑admin users are limited to
editing only a predefined set of fields.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other non‑sensitive fields as needed
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee profile dictionary.

    Parameters
    ----------
    person : dict
        The original employee profile.
    alterations : dict
        Keys are field names to update; values are the new values.
    has_admin_rights : bool
        ``True`` if the caller is an admin and may modify any field.
        ``False`` limits modifications to :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field outside
        :data:`EDITABLE_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_profile = dict(person)

    for field, new_value in alterations.items():
        # Determine whether the change is permitted
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Perform the update
        updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (for local testing only; remove or guard under `if __name__ == "__main__":` in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_person = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 90000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change position (allowed)
    try:
        print(
            adjust_employee_details(
                person=sample_person,
                alterations={"position": "Senior Engineer"},
                has_admin_rights=False,
            )
        )
    except ValueError as e:
        print(e)

    # Non‑admin attempting to change salary (disallowed)
    try:
        print(
            adjust_employee_details(
                person=sample_person,
                alterations={"salary": 95000},
                has_admin_rights=False,
            )
        )
    except ValueError as e:
        print(e)

    # Admin updating any field
    print(
        adjust_employee_details(
            person=sample_person,
            alterations={"salary": 95000, "department": "Engineering"},
            has_admin_rights=True,
        )
    )