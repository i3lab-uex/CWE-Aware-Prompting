#!/usr/bin/env python3
"""
Employee profile adjustment utility.

This module defines a single public function, `adjust_employee_details`, that
updates an employee profile dictionary with supplied alterations.  Only a
whitelisted set of keys may be modified by non‑admin users.

The module is deliberately lightweight and contains no external dependencies.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin user is allowed to edit.  Admins may modify any
#: field present in the profile dictionary.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: `salary` and `social_security_number` are deliberately omitted
    # to prevent accidental or malicious changes by non‑admin users.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: dict,
    alterations: dict,
    has_admin_rights: bool
) -> dict:
    """
    Update an employee profile with a set of alterations.

    Parameters
    ----------
    person : dict
        The current employee profile.  It must be a mapping from field names to
        values.  This dictionary is *not* modified in place; a new dictionary
        containing the updated values is returned.
    alterations : dict
        A mapping from field names to new values that should be applied to the
        profile.
    has_admin_rights : bool
        ``True`` if the caller is an administrator; otherwise the function
        will restrict updates to :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If an alteration attempts to modify a field that is not present in the
        original profile, or if a non‑admin user tries to modify a field that
        is not in :data:`EDITABLE_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of the input profile before applying
    changes, ensuring that callers are not affected by side effects.  The copy
    is shallow because nested mutable objects (e.g., lists or dicts) are not
    expected to be part of the employee profile in this context.

    Examples
    --------
    >>> original = {'name': 'Alice', 'position': 'Engineer',
    ...              'salary': 90000, 'department': 'R&D'}
    >>> alterations = {'position': 'Senior Engineer', 'salary': 95000}
    >>> adjust_employee_details(original, alterations, has_admin_rights=True)
    {'name': 'Alice', 'position': 'Senior Engineer',
     'salary': 95000, 'department': 'R&D'}
    >>> adjust_employee_details(original, alterations, has_admin_rights=False)
    {'name': 'Alice', 'position': 'Senior Engineer',
     'salary': 90000, 'department': 'R&D'}
    """
    if not isinstance(person, dict):
        raise TypeError("`person` must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("`alterations` must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("`has_admin_rights` must be a boolean")

    # Create a shallow copy to avoid mutating the caller's dictionary
    updated = dict(person)

    for key, new_value in alterations.items():
        if key not in person:
            raise ValueError(f"Field '{key}' does not exist in the employee profile")

        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'"
            )

        # Basic type checking: preserve original type to avoid accidental
        # coercion.  This is optional but helps catch obvious bugs.
        original_type = type(person[key])
        if not isinstance(new_value, original_type):
            # Allow None for optional fields
            if new_value is not None:
                raise TypeError(
                    f"Field '{key}' expects a value of type {original_type.__name__}"
                )

        updated[key] = new_value

    return updated