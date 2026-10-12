#!/usr/bin/env python3
"""
Utility to safely adjust employee profile details.

The module enforces strict field‑level permissions, preventing
non‑admin users from modifying sensitive attributes such as
social_security_number or salary.  It also protects against
CWE‑913 by ensuring only explicitly whitelisted fields are
modified, even when the underlying data structures are dynamic.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin user is allowed to edit.  All other fields are
#: considered protected and may only be changed by an administrator.
EDITABLE_FIELDS: frozenset[str] = frozenset(
    {"name", "position", "department", "email", "phone_number"}
)


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes
    applied.

    Parameters
    ----------
    person : dict
        Current employee profile.  Keys represent field names; values may be of
        any JSON‑serialisable type.
    alterations : dict
        Mapping from field names to the new values that should be applied.
    has_admin_rights : bool
        ``True`` if the caller is an administrator and may modify any field;
        otherwise only fields in :data:`EDITABLE_FIELDS` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The input ``person``
        is left untouched.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a protected field, or if an
        alteration refers to a key that does not exist in the original profile.
    TypeError
        If ``person`` or ``alterations`` is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of ``person`` before applying any
      changes.  If nested mutable objects are present, they are shared between
      the original and the returned dictionary.  This is intentional: it keeps
      memory usage low while still preventing accidental mutation of the
      caller's dictionary.
    * The function does **not** validate data types for individual fields;
      callers should ensure that ``alterations`` contains values of the
      expected type.
    """

    # Input validation ----------------------------------------------------- #
    if not isinstance(person, dict):
        raise TypeError("`person` must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("`alterations` must be a dictionary")

    # Prepare the result ---------------------------------------------------- #
    updated = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Reject unknown fields – we don't want to create attributes silently
        if field not in person:
            raise ValueError(f"Field '{field}' does not exist in the employee profile")

        # Permission check --------------------------------------------------- #
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify protected field '{field}'"
            )

        # Apply the change --------------------------------------------------- #
        updated[field] = new_value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee profile
    emp = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
        "email": "alice@example.com",
    }

    # Non‑admin attempt to change salary – should raise ValueError
    try:
        adjust_employee_details(emp, {"salary": 95000}, has_admin_rights=False)
    except ValueError as exc:
        print(f"Access denied: {exc}")

    # Admin changing salary
    updated_emp = adjust_employee_details(emp, {"salary": 95000}, has_admin_rights=True)
    print("Updated profile:", updated_emp)