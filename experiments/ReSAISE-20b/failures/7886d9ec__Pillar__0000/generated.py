# -*- coding: utf-8 -*-
"""
Employee profile adjustment module.

This module defines a single public function, `adjust_employee_details`,
which updates an employee profile dictionary with new values provided by
the caller.  The function enforces that only a predefined set of fields can
be edited by non‑admin users, protecting sensitive data such as the
`social_security_number`.  It raises a ValueError if an attempt is made to
modify a disallowed field.

The implementation avoids external dependencies and performs defensive
copying of the input dictionary to prevent accidental mutation of caller
state.  It also guards against CWE‑664 by ensuring that the dictionary
resource is fully controlled within this function and no dangling references
are returned.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to edit.  All other fields
# are considered read‑only for normal users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is deliberately omitted to prevent accidental wage changes
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
    Update an employee profile dictionary with new values.

    Parameters
    ----------
    person : dict
        Current employee profile.  Must be a mapping of attribute names to
        values.
    alterations : dict
        Mapping of fields that should be updated and their new values.
    has_admin_rights : bool
        Flag indicating whether the caller is an admin.  Admin users may
        modify any field; non‑admins are restricted to EDITABLE_FIELDS.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.  The
        original ``person`` mapping is not modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in EDITABLE_FIELDS,
        or if an attempt is made to change the `social_security_number`
        without admin rights.

    Notes
    -----
    * The function performs a shallow copy of ``person``; nested mutable
      values are not deeply copied.  This is sufficient for typical employee
      profile structures.
    * The function is deliberately pure: it does not perform I/O or
      external side‑effects, which helps mitigate CWE‑664 concerns.
    """
    # Defensive copy to avoid mutating caller's data
    updated_profile = dict(person)

    for field, new_value in alterations.items():
        # 1. Admins may modify any field
        if has_admin_rights:
            updated_profile[field] = new_value
            continue

        # 2. Non‑admins are restricted to EDITABLE_FIELDS
        if field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be modified by non‑admin users."
            )

        # 3. Explicitly forbid changing sensitive data
        if field == "social_security_number":
            raise ValueError(
                "Modification of 'social_security_number' requires admin rights."
            )

        updated_profile[field] = new_value

    return updated_profile