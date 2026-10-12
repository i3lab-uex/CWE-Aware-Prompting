# -*- coding: utf-8 -*-
"""
Utility module for editing employee profiles with permission checks.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool
) -> Dict[str, Any]:
    """
    Update an employee profile with the supplied changes.

    Parameters
    ----------
    worker : dict
        The current employee profile. Keys are attribute names.
    changes : dict
        A mapping of fields to new values that should be applied.
    is_privileged : bool
        ``True`` if the caller has admin rights; otherwise only editable fields may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field, or if the change references
        a field that does not exist in the original profile.
    """
    # Create a copy so we do not mutate the input dictionary
    updated = deepcopy(worker)

    for field, new_value in changes.items():
        # Ensure the field exists in the profile
        if field not in worker:
            raise ValueError(f"Field '{field}' does not exist in the employee profile.")

        # Enforce permission checks for non‑admin users
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify '{field}'. "
                "Only editable fields can be changed by non‑admin users."
            )

        # Apply the change
        updated[field] = new_value

    return updated