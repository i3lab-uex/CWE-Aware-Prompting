# -*- coding: utf-8 -*-
"""
Employee profile adjustment module.

This module provides a single function, :func:`adjust_employee_profile`, which
updates an employee dictionary in a controlled manner.  Only users with admin
rights may modify any attribute; regular users are restricted to a predefined
set of editable fields.  The function returns a new dictionary and never mutates
the input ``emp`` argument, preventing accidental side‑effects.

The implementation follows best practices for secure programming:
* Defensive copying of mutable objects.
* Explicit validation of requested changes.
* Clear error messages for unauthorized modifications.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# The set of keys that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class UnauthorizedFieldModificationError(RuntimeError):
    """Raised when a user attempts to modify a field they are not permitted to."""
    pass

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_profile(
    emp: dict,
    changes: dict,
    has_admin_rights: bool
) -> dict:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp : dict
        The original employee record.  Must contain string keys.
    changes : dict
        Mapping of field names to new values that the caller wishes to apply.
    has_admin_rights : bool
        ``True`` if the caller is an administrator and may modify any field;
        otherwise only fields in :data:`EDITABLE_FIELDS` are permitted.

    Returns
    -------
    dict
        A shallow copy of ``emp`` with the authorised changes applied.

    Raises
    ------
    UnauthorizedFieldModificationError
        If a non‑admin attempts to modify a field outside ``EDITABLE_FIELDS``.
    TypeError
        If any argument is not of the expected type.
    """
    # --------------------------------------------------------------------- #
    # Input validation
    # --------------------------------------------------------------------- #
    if not isinstance(emp, dict):
        raise TypeError(f"emp must be a dict; got {type(emp).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict; got {type(changes).__name__}")
    if not isinstance(has_admin_rights, bool):
        raise TypeError(f"has_admin_rights must be a bool; got {type(has_admin_rights).__name__}")

    # --------------------------------------------------------------------- #
    # Prepare the result dictionary (shallow copy to avoid mutating input)
    # --------------------------------------------------------------------- #
    updated_emp = emp.copy()

    # --------------------------------------------------------------------- #
    # Apply changes with permission checks
    # --------------------------------------------------------------------- #
    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise TypeError(f"Field names must be strings; got {type(field).__name__}")

        if has_admin_rights:
            # Admin can modify any field
            updated_emp[field] = new_value
        else:
            # Non‑admin: enforce editable fields only
            if field not in EDITABLE_FIELDS:
                raise UnauthorizedFieldModificationError(
                    f"Non‑admin users cannot modify the field '{field}'."
                )
            updated_emp[field] = new_value

    return updated_emp