#!/usr/bin/env python3
"""
Employee profile adjustment utility.

This module defines a single public function, `adjust_employee_details`, which
updates an employee profile dictionary according to the supplied alterations.
The update is constrained by the global constant `EDITABLE_FIELDS` when the
caller does not have administrative rights.

The implementation guards against accidental modification of non‑editable
attributes and protects against the CWE‑913 vulnerability by not allowing
arbitrary code execution or attribute injection.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add additional safe fields here.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested alterations
    applied.

    Parameters
    ----------
    person : dict
        The original employee profile. Must be a flat dictionary.
    alterations : dict
        A mapping of fields to new values that the caller wishes to apply.
    has_admin_rights : bool
        If ``True``, all fields in ``alterations`` are applied.  If ``False``,
        only keys listed in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A shallow copy of ``person`` with the applied changes.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a disallowed field.
    TypeError
        If ``person`` or ``alterations`` is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy; nested mutable objects are shared.
    * Only top‑level keys are considered.  Nested updates would require a
      recursive strategy which is intentionally omitted to avoid accidental
      modification of protected data.
    """
    if not isinstance(person, dict):
        raise TypeError("`person` must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("`alterations` must be a dictionary")

    # Create a shallow copy to avoid mutating the original input.
    updated_person = person.copy()

    for key, new_value in alterations.items():
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'."
            )
        # Defensive: ensure we do not accidentally create new keys that are
        # not present in the original profile.  This avoids leaking information.
        if key not in person:
            raise ValueError(f"Field '{key}' does not exist in the employee profile.")
        updated_person[key] = new_value

    return updated_person