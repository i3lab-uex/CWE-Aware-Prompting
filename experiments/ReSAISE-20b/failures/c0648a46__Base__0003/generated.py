# -*- coding: utf-8 -*-
"""
Employee profile modification utility.

This module defines a single public function `modify_employee_profile` that
updates an employee profile dictionary while enforcing field‑level
permissions.  It protects against CWE‑915 by ensuring that only explicitly
allowed keys can be modified when the caller is not privileged.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Note: salary and social_security_number are intentionally omitted.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker:
        The original employee profile.  It is not modified in place.
    changes:
        A mapping of field names to new values.  Only keys present in the
        original profile are considered; unknown keys raise a ``ValueError``.
    is_privileged:
        If ``True``, the caller has admin rights and can modify any field.
        If ``False`` only fields listed in :data:`EDITABLE_FIELDS` may be
        changed.

    Returns
    -------
    dict
        A shallow copy of ``worker`` with the requested updates applied.

    Raises
    ------
    ValueError
        * If ``changes`` contains a key that does not exist in ``worker``.
        * If ``is_privileged`` is ``False`` and a key not in
          :data:`EDITABLE_FIELDS` is attempted to be modified.
    """
    # Validate that all requested keys exist in the original profile
    unknown_keys = set(changes) - set(worker)
    if unknown_keys:
        raise ValueError(f"Attempted to modify unknown fields: {unknown_keys}")

    # Enforce editable field restrictions for non‑privileged users
    if not is_privileged:
        disallowed = set(changes) - EDITABLE_FIELDS
        if disallowed:
            raise ValueError(
                f"Non‑admin users cannot modify fields: {disallowed}"
            )

    # Perform the update on a copy to avoid mutating the input dictionary
    updated_profile = copy.deepcopy(worker)
    for key, value in changes.items():
        updated_profile[key] = value

    return updated_profile