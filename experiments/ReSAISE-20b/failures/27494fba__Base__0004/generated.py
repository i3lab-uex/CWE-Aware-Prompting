#!/usr/bin/env python3
"""
Utility for safely adjusting employee profiles.

The module protects against CWE-915 by strictly controlling which attributes
may be modified when the caller does not have administrative privileges.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration: Fields that can be edited by regular users
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "department"}  # salary and SSN are protected

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp : dict
        Original employee data. Must contain keys for all fields that can be edited.
    changes : dict
        Proposed modifications. Keys must correspond to employee attributes.
    has_admin_rights : bool
        If True, the caller may modify any attribute. Otherwise only
        ``EDITABLE_FIELDS`` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑editable field is attempted to be modified, or if an unknown
        attribute is referenced.
    """
    # Defensive copy to avoid mutating the caller's dictionary
    updated_emp = copy.deepcopy(emp)

    # Determine which fields are allowed to be changed
    if has_admin_rights:
        allowed_fields = set(emp.keys())
    else:
        allowed_fields = EDITABLE_FIELDS

    for field, new_value in changes.items():
        if field not in allowed_fields:
            raise ValueError(
                f"Modification of field '{field}' is not permitted for "
                f"{'admin' if has_admin_rights else 'regular'} users."
            )
        if field not in emp:
            raise ValueError(f"Unknown employee attribute: '{field}'.")
        updated_emp[field] = new_value

    return updated_emp