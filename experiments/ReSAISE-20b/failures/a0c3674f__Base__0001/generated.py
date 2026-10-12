# -*- coding: utf-8 -*-
"""
Utility for safely updating employee records.

This module provides the `modify_staff_info` function, which applies a set of
changes to an employee dictionary while enforcing strict access controls.

The primary security concern addressed here is CWE‑915: *Improperly
Controlled Modification of Dynamically-Determined Object Attributes*.
By limiting updates to a predefined whitelist (`EDITABLE_FIELDS`) and
rejecting any other keys, we ensure that only authorized attributes can be
modified.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# Global whitelist of fields that non‑admin users may modify.
EDITABLE_FIELDS: Iterable[str] = (
    "name",
    "position",
    "salary",
    "department",
)

def _is_valid_field(field: str) -> bool:
    """
    Internal helper to check whether a field is allowed for modification.

    Parameters
    ----------
    field : str
        The attribute name to check.

    Returns
    -------
    bool
        ``True`` if the field is in the whitelist; otherwise, ``False``.
    """
    return field in EDITABLE_FIELDS

def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Apply a set of changes to an employee record in a controlled manner.

    Parameters
    ----------
    staff : dict
        Current state of the employee's details.  The dictionary may contain
        arbitrary keys, but only those listed in ``EDITABLE_FIELDS`` are
        modifiable by non‑admin users.
    changes : dict
        Key/value pairs describing the desired updates.  Keys that are not
        permitted for modification will cause a ``ValueError`` to be raised.
    admin_status : bool
        Flag indicating whether the caller has administrative privileges.  If
        ``True``, all keys in ``changes`` are applied; otherwise, only keys
        present in ``EDITABLE_FIELDS`` may be updated.

    Returns
    -------
    dict
        A new dictionary containing the original employee data with the valid
        updates applied.  The input ``staff`` dictionary is not modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not present in
        ``EDITABLE_FIELDS``.
    TypeError
        If either ``staff`` or ``changes`` is not a mapping type.

    Notes
    -----
    * The function performs a shallow copy of ``staff``; nested mutable values
      are not deep‑cloned.
    * No attempt is made to validate the data types of new values; callers
      should perform domain‑specific validation if required.
    """
    # Basic type checks to avoid unexpected errors later
    if not isinstance(staff, dict):
        raise TypeError("staff must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a copy so the original is left untouched
    updated_staff = copy.deepcopy(staff)

    # Iterate over requested changes
    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise ValueError(f"Field name must be a string; got {field!r}")

        # Admins bypass the whitelist
        if admin_status or _is_valid_field(field):
            updated_staff[field] = new_value
        else:
            # Disallowed field modification attempted by a non‑admin
            raise ValueError(
                f"Non-admin users cannot modify the field '{field}'."
            )

    return updated_staff