# -*- coding: utf-8 -*-
"""
Employee data modification module.

This module defines a single function `modify_employee_data` that safely updates
employee records represented as dictionaries.  The implementation guards against
unauthorized field modifications, protects sensitive data from accidental
overwrites, and follows the security guidelines for CWE‑913.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that a regular (non‑admin) user is allowed to modify.
EDITABLE_FIELDS: set[str] = {"name", "position", "department"}

# Fields that are considered sensitive and should never be altered by a regular
# user, even if they happen to exist in the `EDITABLE_FIELDS` set.
SENSITIVE_FIELDS: set[str] = {"social_security_number", "salary"}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _validate_field_names(
    alterations: dict[str, any],
    worker_fields: set[str],
    admin_privileges: bool,
) -> None:
    """
    Validate that the requested alterations are permissible.

    Parameters
    ----------
    alterations : dict[str, any]
        Proposed changes.
    worker_fields : set[str]
        Set of existing keys in the employee dictionary.
    admin_privileges : bool
        True if the caller has administrative rights.

    Raises
    ------
    ValueError
        If an unauthorized field is being modified.
    KeyError
        If the alteration references a non‑existent field in the worker dict.
    """
    for key in alterations:
        if key not in worker_fields:
            raise KeyError(f"Field '{key}' does not exist in the employee record.")

        if not admin_privileges:
            # Non‑admin users may only touch EDITABLE_FIELDS and must not
            # modify sensitive fields.
            if key in SENSITIVE_FIELDS:
                raise ValueError(f"Modification of sensitive field '{key}' is forbidden.")
            if key not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify field '{key}'. "
                    f"Allowed fields: {sorted(EDITABLE_FIELDS)}."
                )

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def modify_employee_data(
    worker: dict[str, any],
    alterations: dict[str, any],
    admin_privileges: bool,
) -> dict[str, any]:
    """
    Safely update an employee dictionary with the provided alterations.

    The function ensures that:
      * Only existing fields are touched.
      * Regular users may only modify fields listed in EDITABLE_FIELDS and
        never sensitive data such as social security numbers or salaries.
      * Admin users have full control over all fields.

    Parameters
    ----------
    worker : dict[str, any]
        The original employee record.
    alterations : dict[str, any]
        Proposed changes to apply to the employee record.
    admin_privileges : bool
        Flag indicating whether the caller has administrative rights.

    Returns
    -------
    dict[str, any]
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If an alteration references a field that does not exist in the worker.
    ValueError
        If a non‑admin attempts to modify an unauthorized field or sensitive data.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary.")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary.")

    # Copy the worker to avoid mutating the original reference.
    updated_worker = worker.copy()

    # Validate alterations before applying them.
    _validate_field_names(
        alterations=alterations,
        worker_fields=set(updated_worker.keys()),
        admin_privileges=admin_privileges,
    )

    # Apply the changes safely.
    for key, value in alterations.items():
        updated_worker[key] = value

    return updated_worker