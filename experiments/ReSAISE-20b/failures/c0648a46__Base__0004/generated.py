#!/usr/bin/env python3
"""
Employee profile modifier with safe attribute updates.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

# Fields that are protected and can only be modified by a privileged user.
PROTECTED_FIELDS = {"salary", "social_security_number"}

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile safely.

    Parameters
    ----------
    worker : dict
        The current employee profile.
    changes : dict
        Dictionary of fields to update with their new values.
    is_privileged : bool
        True if the caller has admin rights; otherwise False.

    Returns
    -------
    dict
        A new dictionary representing the updated profile.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify an uneditable field,
        or if any key in ``changes`` does not exist in the original profile.
    """
    # Make a shallow copy to avoid mutating the caller's dict
    updated = copy.deepcopy(worker)

    for field, new_value in changes.items():
        # Reject attempts to modify unknown fields
        if field not in worker:
            raise ValueError(f"Field '{field}' does not exist in the profile.")

        # Non‑admin users can only modify fields listed in EDITABLE_FIELDS
        if not is_privileged:
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑privileged users cannot modify the field '{field}'."
                )
        else:
            # Admins may change any existing field; no further checks needed
            pass

        updated[field] = new_value

    return updated