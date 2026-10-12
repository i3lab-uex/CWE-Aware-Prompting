# -*- coding: utf-8 -*-

"""
Utility module for editing employee records with role‑based permissions.
"""

from __future__ import annotations

# Fields that can be edited by non‑admin users
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def edit_personnel_info(
    employee_record: dict,
    adjustments: dict,
    admin_flag: bool
) -> dict:
    """
    Return an updated employee record after applying the allowed adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's data.  Keys must include at least
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    adjustments : dict
        Mapping of field names to new values that should be applied.
    admin_flag : bool
        ``True`` if the caller has administrative privileges; otherwise only
        fields listed in :data:`EDITABLE_FIELDS` may be modified.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.

    Raises
    ------
    KeyError
        If an adjustment refers to a field that does not exist in the record.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    TypeError
        If ``employee_record`` or ``adjustments`` are not dictionaries.

    Notes
    -----
    - The original ``employee_record`` is never mutated; a shallow copy is returned.
    - Sensitive fields such as ``social_security_number`` can only be altered by
      admins.  Attempts to modify them by non‑admins raise ``PermissionError``.
    """
    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")

    # Create a shallow copy to avoid side‑effects
    updated_record = employee_record.copy()

    for field, new_value in adjustments.items():
        if field not in updated_record:
            raise KeyError(f"Field '{field}' does not exist in the employee record")

        # Non‑admins can only modify allowed fields
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Insufficient privileges to modify the field '{field}'"
            )

        updated_record[field] = new_value

    return updated_record