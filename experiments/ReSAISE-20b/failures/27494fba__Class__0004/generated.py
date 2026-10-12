# -*- coding: utf-8 -*-
"""
Utility to adjust an employee profile while respecting edit permissions.
"""

from typing import Dict, Any

# Fields that a regular user is allowed to modify
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other non‑sensitive fields here
}

def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool
) -> Dict[str, Any]:
    """
    Update an employee dictionary with the supplied changes.

    Parameters
    ----------
    emp : dict
        The original employee record.
    changes : dict
        Mapping of attribute names to new values.
    has_admin_rights : bool
        If True, all fields may be updated; otherwise only those in
        ``EDITABLE_FIELDS`` are permitted.

    Returns
    -------
    dict
        The updated employee record (the same object as ``emp``).

    Raises
    ------
    ValueError
        If ``changes`` contains keys that are not present in ``emp``
        or, for non‑admin users, keys outside the allowed set.
    """
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    for key, value in changes.items():
        if key not in emp:
            raise ValueError(f"Attempted to modify unknown field: {key!r}")

        # Non‑admin users can only edit allowed fields
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field: {key!r}"
            )

        # Assign the new value safely; no code execution is performed.
        emp[key] = value

    return emp