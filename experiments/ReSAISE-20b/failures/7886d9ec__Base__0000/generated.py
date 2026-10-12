#!/usr/bin/env python3
"""
Employee profile updater with strict field control.

CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non-admin users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Non-admin users cannot modify salary or SSN.
}

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested alterations applied.

    Parameters
    ----------
    person : dict
        Current employee profile.
    alterations : dict
        Fields and new values to apply.
    has_admin_rights : bool
        True if the caller has admin privileges.

    Returns
    -------
    dict
        Updated employee profile.

    Raises
    ------
    ValueError
        If a non-admin attempts to modify a protected field.
    KeyError
        If an alteration references a key that does not exist in the profile.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_profile = deepcopy(person)

    for field, new_value in alterations.items():
        # Ensure the field exists in the original profile
        if field not in updated_profile:
            raise KeyError(f"Field '{field}' does not exist in the employee profile.")

        # Enforce field-level permissions
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Unauthorized modification of protected field '{field}'. "
                "Only admins may alter this attribute."
            )

        # Apply the alteration
        updated_profile[field] = new_value

    return updated_profile