#!/usr/bin/env python3
"""
Secure employee detail modification module.

This module implements a single public function, `modify_staff_details`,
which applies user‑requested changes to an employee record while enforcing
strict field‑level access control.  Regular users are allowed to modify only
the fields defined in the global `EDITABLE_FIELDS` set.  Superusers are
unrestricted.

The implementation follows best practices to mitigate CWE‑915
(Improperly Controlled Modification of Dynamically‑Determined Object
Attributes) by validating every key in `changes` against the allowed set
and raising a descriptive exception if an unauthorized field is requested.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that non‑superusers are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_staff_details(
    employee_data: dict,
    changes: dict,
    is_superuser: bool
) -> dict:
    """
    Apply a set of changes to an employee record while enforcing access control.

    Parameters
    ----------
    employee_data : dict
        The original employee record.  It must be a mapping of attribute names to values.
    changes : dict
        Proposed modifications.  Keys are field names, values are the new values.
    is_superuser : bool
        ``True`` if the caller has administrative privileges; otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.  The original
        `employee_data` is left untouched.

    Raises
    ------
    ValueError
        If the caller attempts to modify a field that is not permitted for their role.
    TypeError
        If `employee_data` or `changes` is not a mapping type.

    Notes
    -----
    * The function performs shallow copies; nested mutable objects are shared.
      This is acceptable because the function only updates top‑level keys.
    * Keys that are present in `changes` but absent from `employee_data`
      are added to the resulting dictionary (subject to permission checks).
    """
    # Basic type validation
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Determine which fields the caller is allowed to modify
    if is_superuser:
        allowed_fields = set(employee_data.keys()).union(changes.keys())
    else:
        allowed_fields = EDITABLE_FIELDS

    # Verify that every requested change is permitted
    for field in changes:
        if field not in allowed_fields:
            raise ValueError(
                f"Modification of field '{field}' is not permitted for this user"
            )

    # Create a shallow copy to avoid mutating the original record
    updated = employee_data.copy()

    # Apply allowed changes
    for field, new_value in changes.items():
        updated[field] = new_value

    return updated