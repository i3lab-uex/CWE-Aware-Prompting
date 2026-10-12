# -*- coding: utf-8 -*-
"""
Employee record update utility.

The module defines a single function `alter_employee_details` that applies
changes to an employee dictionary while enforcing field‑level permissions.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

# Immutable fields that should never be altered by any user.
IMMUTABLE_FIELDS = {
    "social_security_number",
}

def _sanitize_key(key: str) -> bool:
    """
    Basic sanity check to ensure the key contains only allowed characters.
    This prevents attempts to inject malicious keys such as '__class__' or
    other special attributes that could lead to attribute injection.
    """
    return key.isidentifier() and not key.startswith("_")

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Apply a set of changes to an employee record with proper permission checks.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's record.
    changes : dict
        Proposed field updates. Keys are attribute names, values are new data.
    is_superuser : bool
        Flag indicating if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If any change attempts to modify an immutable field or a field that
        is not allowed for the current user level.
    KeyError
        If a requested field does not exist in the employee record.
    """
    # Create a shallow copy to avoid mutating the original input
    updated = deepcopy(emp_data)

    for key, new_value in changes.items():
        # Basic validation of the field name
        if not _sanitize_key(key):
            raise ValueError(f"Invalid field name: {key!r}")

        # Ensure the key exists in the record
        if key not in updated:
            raise KeyError(f"Field '{key}' does not exist in employee record")

        # Prevent modification of immutable fields
        if key in IMMUTABLE_FIELDS:
            raise ValueError(f"Field '{key}' is immutable and cannot be changed")

        # Enforce permission based on user role
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify field '{key}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated[key] = new_value

    return updated