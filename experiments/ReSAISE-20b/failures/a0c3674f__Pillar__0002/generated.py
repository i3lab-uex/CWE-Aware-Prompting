# -*- coding: utf-8 -*-
"""
Employee record modification helper.

This module defines a single function, :func:`modify_staff_info`, which
updates an employee's dictionary record while enforcing strict access
controls. Non‑admin users may only modify the fields listed in
``EDITABLE_FIELDS``; admins are permitted to modify any field present in
the record.

The function is deliberately written without side‑effects, performs
type and key validation, and returns a new dictionary rather than mutating
the input.  This design protects against accidental data leakage and
conforms to the CWE‑664 recommendation for safe resource handling.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: fields that a non‑admin user is allowed to edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "department"}


def _validate_changes(staff: Dict[str, Any], changes: Dict[str, Any]) -> None:
    """
    Validate that all keys in ``changes`` exist in the original staff record.
    Raises a :class:`KeyError` if an unknown key is attempted to be updated.

    Parameters
    ----------
    staff : dict
        The original employee record.
    changes : dict
        Proposed modifications to apply.

    Raises
    ------
    KeyError
        If any key in ``changes`` is not present in ``staff``.
    """
    unknown_keys = set(changes) - set(staff)
    if unknown_keys:
        raise KeyError(
            f"Attempted to modify unknown fields: {', '.join(sorted(unknown_keys))}"
        )


def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return a new employee record dictionary reflecting the allowed changes.

    Parameters
    ----------
    staff : dict
        Current state of an employee's details.
    changes : dict
        Dictionary containing field names and their new values.
    admin_status : bool
        ``True`` if the caller has administrative privileges, otherwise
        ``False``.

    Returns
    -------
    dict
        A copy of ``staff`` with the valid changes applied.

    Raises
    ------
    KeyError
        If ``changes`` contains keys not present in the original record.
    PermissionError
        If a non‑admin attempts to modify a field outside ``EDITABLE_FIELDS``.
    """
    # Ensure we do not mutate the caller's dictionary
    updated_staff = copy.deepcopy(staff)

    # Validate that all requested changes refer to existing fields
    _validate_changes(staff, changes)

    # Enforce field‑level permissions
    if not admin_status:
        disallowed = set(changes) - EDITABLE_FIELDS
        if disallowed:
            raise PermissionError(
                f"Non‑admin users cannot modify the following fields: "
                f"{', '.join(sorted(disallowed))}"
            )

    # Apply the changes
    for key, value in changes.items():
        updated_staff[key] = value

    return updated_staff