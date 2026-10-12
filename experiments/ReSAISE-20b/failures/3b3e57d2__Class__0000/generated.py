# -*- coding: utf-8 -*-

"""
Employee data modification module.

The function ``modify_staff_details`` safely updates an employee dictionary
according to the rules described in the task.  It protects against
unintended or malicious modifications by enforcing a whitelist of editable
fields for regular users, while allowing superusers to modify any field.

Security consideration:
    CWE-913: Improper Control of Dynamically-Managed Code Resources
    The implementation uses a strict whitelist and avoids executing or
    evaluating any user-supplied code.  All updates are performed via the
    standard ``dict`` operations, which do not execute arbitrary code.
"""

from __future__ import annotations

# Whitelist of fields that a regular user may edit
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_staff_details(
    employee_data: dict,
    changes: dict,
    is_superuser: bool
) -> dict:
    """
    Update an employee's data according to the supplied changes.

    Parameters
    ----------
    employee_data : dict
        Current employee record.  Must be a mapping of field names to values.
    changes : dict
        Proposed modifications, mapping field names to new values.
    is_superuser : bool
        ``True`` if the caller has administrative privileges; otherwise
        only fields in :data:`EDITABLE_FIELDS` may be modified.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``employee_data`` is not modified in place.

    Raises
    ------
    ValueError
        If a regular user attempts to modify a field that is not in
        :data:`EDITABLE_FIELDS`.
    TypeError
        If ``employee_data`` or ``changes`` is not a mapping type.
    """
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a copy to avoid mutating the original
    updated = employee_data.copy()

    for field, new_value in changes.items():
        if is_superuser:
            # Superusers may modify any field
            updated[field] = new_value
        else:
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Field '{field}' is not editable for regular users."
                )
            updated[field] = new_value

    return updated