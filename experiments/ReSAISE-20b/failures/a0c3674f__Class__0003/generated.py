#!/usr/bin/env python3
"""
Safe staff record modifier.

This module defines a single function `modify_staff_info` that updates an
employee dictionary only with permitted fields.  It is intentionally free of
dynamic code execution and limits write access to a controlled set of keys,
protecting against CWE‑913 (Improper Control of Dynamically-Managed Code
Resources).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global list of fields that non‑admin users may modify.
EDITABLE_FIELDS = {"name", "position", "department"}


def _is_valid_field(field: str) -> bool:
    """
    Check whether a field is present in the staff record and is safe to modify.
    This helper prevents accidental creation of new keys or modification of
    protected fields such as 'salary' or 'social_security_number'.
    """
    return field in EDITABLE_FIELDS


def modify_staff_info(staff: Dict[str, Any],
                      changes: Dict[str, Any],
                      admin_status: bool) -> Dict[str, Any]:
    """
    Return an updated copy of *staff* with only the allowed changes applied.

    Parameters
    ----------
    staff : dict
        Current employee record.  Expected keys include at least:
        'name', 'position', 'salary', 'department',
        and 'social_security_number'.
    changes : dict
        Proposed updates.  Keys are field names; values are the new data.
    admin_status : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary reflecting the validated changes.  The original
        ``staff`` dictionary is left untouched.

    Raises
    ------
    ValueError
        If any key in *changes* is not a known field, or if a non‑admin
        attempts to modify a protected field.
    """
    # Create a shallow copy so the original dict remains unchanged
    updated_staff = copy.deepcopy(staff)

    for field, new_value in changes.items():
        # Ensure the key exists in the original record
        if field not in staff:
            raise ValueError(f"Unknown field '{field}' cannot be updated.")

        # Non‑admin users are restricted to EDITABLE_FIELDS
        if not admin_status and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field '{field}'."
            )

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff