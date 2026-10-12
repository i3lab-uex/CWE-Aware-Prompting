from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add any other fields that should be editable by non‑admins here.
}


def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile with the provided alterations.

    Parameters
    ----------
    person : dict
        The current employee profile.
    alterations : dict
        Dictionary of field names to new values that should be applied.
    has_admin_rights : bool
        If ``True`` the caller is an administrator and may modify any field.
        If ``False`` only fields listed in :data:`EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a field that is not in
        :data:`EDITABLE_FIELDS`.
    KeyError
        If an alteration refers to a field that does not exist in ``person``.
    """
    # Work on a shallow copy to avoid mutating the original dictionary.
    updated = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Ensure the field exists in the original profile.
        if field not in person:
            raise KeyError(f"Field '{field}' does not exist in the employee profile.")

        # Enforce edit permissions.
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change.
        updated[field] = new_value

    return updated