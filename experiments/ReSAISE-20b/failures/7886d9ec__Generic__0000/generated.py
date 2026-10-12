from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify
EDITABLE_FIELDS = {"name", "position", "department"}

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile with the requested modifications applied.

    Parameters
    ----------
    person : dict
        Current employee profile.
    alterations : dict
        Dictionary of fields to update with their new values.
    has_admin_rights : bool
        True if the caller is an administrator.

    Raises
    ------
    ValueError
        If a non‑admin attempts to change a disallowed field, or if any
        alteration references a key that does not exist in the profile.
    """
    # Make a shallow copy so the original dictionary is unchanged
    updated = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Ensure the field exists
        if field not in person:
            raise ValueError(f"Field '{field}' does not exist in the employee profile.")

        # Non‑admin users can only modify allowed fields
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient rights to modify field '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated[field] = new_value

    return updated