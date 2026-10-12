# -*- coding: utf-8 -*-
"""
Utility module for employee data modification.

The `modify_staff_details` function updates an employee record according
to a set of allowed editable fields.  Regular users may only modify the
fields listed in `EDITABLE_FIELDS`.  Super‑users (administrators) may
modify any field.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

#: Fields that a non‑superuser is allowed to edit.
EDITABLE_FIELDS: set[str] = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_changes(changes: Dict[str, Any]) -> None:
    """
    Validate the `changes` mapping.

    Raises
    ------
    TypeError
        If `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not a string or if the value is ``None``.
    """
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    for key, value in changes.items():
        if not isinstance(key, str):
            raise ValueError(f"Change key must be a string, got {type(key).__name__}")
        if value is None:
            raise ValueError(f"Change value for key '{key}' cannot be None")


def _is_allowed_field(field: str, is_superuser: bool) -> bool:
    """
    Determine if a field may be edited by the current user.

    Parameters
    ----------
    field : str
        The name of the attribute to be edited.
    is_superuser : bool
        Whether the current user has superuser privileges.

    Returns
    -------
    bool
        ``True`` if the field may be edited, otherwise ``False``.
    """
    return is_superuser or field in EDITABLE_FIELDS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the supplied changes.

    Parameters
    ----------
    employee_data : dict
        Current employee data.  Keys are attribute names.
    changes : dict
        Proposed modifications.  Keys must exist in ``employee_data`` or may be new.
    is_superuser : bool
        ``True`` if the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If a change refers to an unknown field and the user is not superuser.
    PermissionError
        If a regular user attempts to modify a non‑editable field.
    TypeError, ValueError
        For invalid input types or values.

    Notes
    -----
    * The function does **not** modify ``employee_data`` in place; it
      returns a new dictionary.
    * All checks are performed before any modifications are applied,
      ensuring atomicity.

    Examples
    --------
    >>> emp = {'name': 'Alice', 'position': 'Developer', 'salary': 70000}
    >>> modify_staff_details(emp, {'name': 'Alicia'}, False)
    {'name': 'Alicia', 'position': 'Developer', 'salary': 70000}
    >>> modify_staff_details(emp, {'salary': 80000}, False)
    Traceback (most recent call last):
        ...
    PermissionError: Regular users may not modify field 'salary'
    """
    # 1. Basic validation
    if not isinstance(employee_data, dict):
        raise TypeError("`employee_data` must be a dictionary")

    _validate_changes(changes)

    # 2. Determine which changes are allowed
    for field in changes:
        if not _is_allowed_field(field, is_superuser):
            raise PermissionError(
                f"Regular users may not modify field '{field}'"
            )

    # 3. Apply changes atomically
    updated = employee_data.copy()
    for field, value in changes.items():
        # For regular users we already know the field exists.
        if not is_superuser and field not in employee_data:
            raise KeyError(f"Unknown field '{field}' for non‑superuser")
        updated[field] = value

    return updated