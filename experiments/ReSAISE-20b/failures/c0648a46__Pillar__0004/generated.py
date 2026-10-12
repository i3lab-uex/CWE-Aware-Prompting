#!/usr/bin/env python3
"""
Employee profile modifier.

This module defines a function `modify_employee_profile` that safely updates an employee
profile dictionary.  Non‑privileged users are only allowed to modify a predefined set of
fields (`EDITABLE_FIELDS`).  The function returns a new dictionary containing the
updated profile, leaving the original unchanged to avoid accidental side‑effects.

The implementation follows best practices for security and resource management,
preventing inadvertent modification of sensitive data such as social security numbers
or salary information by non‑admin users.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Fields that can be edited by non‑privileged users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: `salary` and `social_security_number` are deliberately omitted.
}


def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Return a modified copy of an employee profile.

    Parameters
    ----------
    worker : dict
        The current employee profile. Must be a mapping of string keys to any values.
    changes : dict
        A mapping of field names to new values that should be applied to the profile.
    is_privileged : bool
        If ``True``, all fields in *changes* are applied.  If ``False`` only
        keys present in :data:`EDITABLE_FIELDS` are considered.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The original *worker*
        dictionary is not modified.

    Raises
    ------
    TypeError
        If *worker* or *changes* is not a dictionary.
    ValueError
        If a non‑privileged user attempts to modify a disallowed field.

    Notes
    -----
    * The function performs a shallow copy of the profile to avoid unintended
      side‑effects.  If the profile contains nested mutable objects they will be
      shared between the original and the copy, which is acceptable for this use‑case.
    * This implementation protects against CWE‑664 by ensuring that the resource
      (the employee profile dictionary) is not left in an inconsistent state if a
      partial update occurs.  By validating all changes before applying them and
      returning a new dictionary, we maintain clear ownership of the resource.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original profile.
    updated_profile = copy.deepcopy(worker)

    # Determine which fields are allowed to be changed.
    if is_privileged:
        allowed_fields = set(worker.keys()) | set(changes.keys())
    else:
        # Non‑privileged users can only change fields listed in EDITABLE_FIELDS.
        allowed_fields = EDITABLE_FIELDS

    # Validate changes before applying them.
    for field, new_value in changes.items():
        if field not in allowed_fields:
            raise ValueError(
                f"Field '{field}' cannot be modified by non‑privileged user."
            )
        # Apply the change.
        updated_profile[field] = new_value

    return updated_profile