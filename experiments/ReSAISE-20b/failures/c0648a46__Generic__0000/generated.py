#!/usr/bin/env python3
"""
Employee profile modification utility.

The module exposes a single function `modify_employee_profile` that updates an
employee dictionary in place while enforcing access control based on the
user's privilege level.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Any, Dict

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def _validate_input(worker: Dict[str, Any], changes: Dict[str, Any]) -> None:
    """
    Basic validation of the input arguments.

    Raises:
        TypeError: if any argument is not a dictionary.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Non‑privileged users may only modify fields listed in ``EDITABLE_FIELDS``.
    Privileged (admin) users can modify any field present in the original profile.

    Parameters
    ----------
    worker : dict
        Current employee profile.
    changes : dict
        Mapping of field names to new values that should be applied.
    is_privileged : bool
        ``True`` if the caller has admin rights; otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to change a protected field.
    KeyError
        If the changes refer to fields that do not exist in ``worker``.
    """
    _validate_input(worker, changes)

    # Make a shallow copy to avoid mutating the original dictionary.
    updated = copy.deepcopy(worker)

    for field, new_value in changes.items():
        if field not in worker:
            raise KeyError(f"Field '{field}' does not exist in the employee profile")

        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑privileged users cannot modify the field '{field}'"
            )

        updated[field] = new_value

    return updated