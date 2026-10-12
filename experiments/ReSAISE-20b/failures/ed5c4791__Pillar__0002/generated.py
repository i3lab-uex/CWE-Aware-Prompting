#!/usr/bin/env python3
"""
Employee data modification module.

This module provides a single public function `modify_employee_data` that updates an
employee dictionary according to a set of proposed alterations. Regular users are only
allowed to modify a pre‑defined subset of fields (`EDITABLE_FIELDS`). Administrators
can change any field.

The implementation performs type checking, input validation and raises a descriptive
exception when an unauthorized modification is attempted.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is permitted to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool = False
) -> dict:
    """
    Apply a set of alterations to an employee dictionary.

    Parameters
    ----------
    worker : dict
        The original employee record. Must be a mapping of attribute names to values.
    alterations : dict
        Proposed changes, mapping attribute names to new values.
    admin_privileges : bool, optional
        If ``True`` the caller has full edit rights. Defaults to ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If ``worker`` or ``alterations`` is not a dictionary.
    ValueError
        If the user does not have permission to modify one or more keys in
        ``alterations``.
    """
    # ------------------------------------------------------------------ #
    # Input validation
    # ------------------------------------------------------------------ #
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")

    # ------------------------------------------------------------------ #
    # Permission check
    # ------------------------------------------------------------------ #
    if not admin_privileges:
        unauthorized_keys = [
            key for key in alterations
            if key not in EDITABLE_FIELDS
        ]
        if unauthorized_keys:
            raise ValueError(
                f"Unauthorized modification attempt for fields: {', '.join(unauthorized_keys)}"
            )

    # ------------------------------------------------------------------ #
    # Apply alterations
    # ------------------------------------------------------------------ #
    updated_worker = worker.copy()
    for key, value in alterations.items():
        # Only update keys that exist in the original worker or allow new keys
        # for admin users. For regular users, we ignore unknown keys silently.
        if key in worker or admin_privileges:
            updated_worker[key] = value

    return updated_worker