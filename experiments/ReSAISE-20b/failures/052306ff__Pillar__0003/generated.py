# -*- coding: utf-8 -*-
"""
Utility module for updating employee records safely.

The function `alter_employee_details` ensures that only authorised fields can be
modified by non‑superusers, protecting sensitive data such as social security
numbers.  It performs a shallow copy of the input dictionary so that callers
are not affected by side‑effects.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by avoiding mutable shared state: the function never mutates the original
`emp_data` dictionary and returns a new instance instead.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that a normal user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp_data : dict
        Current employee record.
    changes : dict
        Mapping of field names to new values.
    is_superuser : bool
        True if the caller has admin privileges.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    PermissionError
        If a non‑superuser attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    KeyError
        If the requested field does not exist in the employee record.
    """
    # Make a deep copy to avoid mutating the original dictionary
    updated = deepcopy(emp_data)

    for field, new_value in changes.items():
        # Verify that the field exists in the original record
        if field not in updated:
            raise KeyError(f"Field '{field}' does not exist in employee record.")

        # Enforce field‑level permissions
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated[field] = new_value

    return updated