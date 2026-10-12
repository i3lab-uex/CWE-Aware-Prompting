# -*- coding: utf-8 -*-

"""
Employee data modification module.

This module defines a single function, `modify_employee_data`, which updates
the attributes of an employee dictionary. The function enforces a strict
whitelist of editable fields for non‑admin users, mitigating the risk of
CWE-915 (Improperly Controlled Modification of Dynamically‑Determined
Object Attributes).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# A set of field names that regular users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

def _validate_alterations(alterations: dict) -> None:
    """
    Validate that all keys in the alterations dictionary are strings.
    Raises a TypeError if any key is not a string.

    Parameters
    ----------
    alterations : dict
        Proposed modifications to an employee's attributes.
    """
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    for key in alterations:
        if not isinstance(key, str):
            raise TypeError(f"Field name must be a string; got {type(key).__name__}")

def modify_employee_data(worker: dict,
                         alterations: dict,
                         admin_privileges: bool) -> dict:
    """
    Update an employee's data according to the provided alterations.

    The function ensures that regular users can only modify a predefined set
    of fields (`EDITABLE_FIELDS`). Administrators bypass this restriction and
    may modify any field present in the `worker` dictionary.

    Parameters
    ----------
    worker : dict
        The original employee record. Expected keys include:
            - name (str)
            - position (str)
            - salary (float or int)
            - department (str)
            - social_security_number (str)
    alterations : dict
        Dictionary of proposed changes. Keys are field names, values are the
        new values to assign.
    admin_privileges : bool
        If True, all fields may be modified. If False, only fields in
        `EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data. The original
        `worker` dictionary is not modified.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a field outside of
        `EDITABLE_FIELDS`.
    TypeError
        If the input types are incorrect.

    Notes
    -----
    - The function performs a shallow copy of the worker dictionary to avoid
      side effects.
    - No dynamic attribute access (e.g., via `eval`) is performed, keeping
      the implementation safe from injection attacks.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    _validate_alterations(alterations)

    # Create a shallow copy to avoid mutating the original dict
    updated_worker = worker.copy()

    for field, new_value in alterations.items():
        # Check if the field exists on the employee record
        if field not in worker:
            raise ValueError(f"Field '{field}' does not exist on the employee record")

        # Enforce editable field restrictions for non‑admin users
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Perform the update
        updated_worker[field] = new_value

    return updated_worker