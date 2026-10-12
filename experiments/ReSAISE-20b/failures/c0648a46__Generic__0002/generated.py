# -*- coding: utf-8 -*-

"""
Employee profile modification utility.

This module provides a single function, `modify_employee_profile`, which
updates an employee's profile dictionary while enforcing field-level
permissions. Non‑admin users may only modify a restricted set of fields,
defined in the `EDITABLE_FIELDS` constant. Admin users (privileged
operators) can modify any field.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_employee_profile(
    worker: dict,
    changes: dict,
    is_privileged: bool = False
) -> dict:
    """
    Modify an employee profile according to the provided changes.

    Parameters
    ----------
    worker : dict
        The current employee profile. Expected to be a dictionary containing
        keys such as ``name``, ``position``, ``salary`` etc.
    changes : dict
        A mapping of field names to new values that should be applied to the
        profile.
    is_privileged : bool, optional
        ``True`` if the caller has administrative privileges and may modify
        any field. Defaults to ``False``.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑privileged caller attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    TypeError
        If either `worker` or `changes` is not a dictionary.

    Notes
    -----
    * The function does **not** modify the original `worker` dictionary in
      place; instead, it returns a new dictionary containing the updates.
    * The function performs no deep copying of nested structures.  If
      nested dictionaries are present and need to be preserved, callers
      should supply a copy beforehand.
    """
    # Basic type checks for robustness
    if not isinstance(worker, dict):
        raise TypeError(f"'worker' must be a dict; got {type(worker).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dict; got {type(changes).__name__}")

    # Enforce permissions for non‑privileged users
    if not is_privileged:
        unauthorized = set(changes) - EDITABLE_FIELDS
        if unauthorized:
            raise ValueError(
                f"Non‑privileged user cannot modify fields: {sorted(unauthorized)}"
            )

    # Create a shallow copy of the original profile to avoid side effects
    updated_profile = worker.copy()

    # Apply changes
    for key, value in changes.items():
        updated_profile[key] = value

    return updated_profile