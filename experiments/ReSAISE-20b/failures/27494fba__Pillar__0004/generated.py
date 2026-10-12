# -*- coding: utf-8 -*-
"""
Employee profile adjustment module.

This module defines a single public function `adjust_employee_profile` that
updates an employee dictionary according to the supplied changes, while
respecting role‑based edit permissions.

The function is intentionally defensive:
* Only keys present in the original employee record are considered.
* Non‑editable fields cannot be altered by regular users.
* Admins can modify any existing field but not add new keys.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration – editable fields for non‑admin users
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}  # salary, social_security_number are protected

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def adjust_employee_profile(
    emp: dict,
    changes: dict,
    has_admin_rights: bool = False,
) -> dict:
    """
    Update an employee dictionary with the supplied changes.

    Parameters
    ----------
    emp : dict
        The original employee record. Must contain keys such as
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    changes : dict
        Proposed modifications. Keys that do not exist in ``emp`` are ignored.
    has_admin_rights : bool, optional
        If True, the caller is an administrator and may modify any existing
        field. Default is False (regular user).

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If ``changes`` attempts to modify a protected field when the caller is
        not an admin.
    TypeError
        If ``emp`` or ``changes`` are not dictionaries.

    Notes
    -----
    * The function does **not** add new keys to the employee record.
    * The original ``emp`` dictionary is left unchanged; a shallow copy is
      returned with the updates applied.
    """
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Start with a shallow copy to avoid mutating the caller's dict
    updated_emp = emp.copy()

    for key, new_value in changes.items():
        if key not in updated_emp:
            # Ignore unknown keys – could log a warning here
            continue

        if has_admin_rights:
            # Admin can modify any existing key
            updated_emp[key] = new_value
        else:
            # Non‑admin: check if the key is editable
            if key in EDITABLE_FIELDS:
                updated_emp[key] = new_value
            else:
                raise ValueError(
                    f"Insufficient privileges to modify '{key}'. "
                    "Only editable fields are allowed."
                )

    return updated_emp