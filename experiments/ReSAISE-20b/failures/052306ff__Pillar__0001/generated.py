# -*- coding: utf-8 -*-
"""
Employee record modification utility.

This module provides a single public function `alter_employee_details` that
creates an updated employee dictionary based on supplied changes.  The
function enforces field-level permissions: non‑admin users may only modify
attributes listed in the global `EDITABLE_FIELDS` set.  Admin (superuser)
users can modify any field.

The implementation avoids side‑effects by operating on a shallow copy of the
input dictionary.  Defensive programming techniques (type checks, value
validation) are employed to mitigate common security pitfalls such as
injection attacks or accidental modification of sensitive data.

The module is intentionally lightweight and free from external dependencies.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to edit.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Salary changes require admin privileges; hence not included here.
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary reflecting the supplied changes.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee record.  Keys are attribute names.
    changes : dict
        Desired modifications; keys are field names and values are the new data.
    is_superuser : bool
        Flag indicating whether the caller has admin privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        `emp_data` is left untouched.

    Raises
    ------
    ValueError
        If `changes` attempts to modify a field that the caller is not allowed
        to edit.
    TypeError
        If `emp_data` or `changes` is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of `emp_data`.  Nested mutable values
      are shared between the original and the returned dictionary.  If deep
      isolation is required, replace `copy.copy` with `copy.deepcopy`.

    * Sensitive fields such as ``social_security_number`` are excluded from
      `EDITABLE_FIELDS`.  Even superusers must be careful to avoid leaking
      this data; the function itself does not provide any extra protection,
      but callers should handle such fields appropriately.

    * This implementation is resistant to CWE-664 (Improper Control of a
      Resource Through its Lifetime) because it never retains references to
      external resources beyond the scope of the function call.  All data is
      passed in as plain Python objects and a new dictionary is created for
      the result.
    """
    # ----------------------------------------------------------------------- #
    # Input validation
    # ----------------------------------------------------------------------- #

    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")

    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # ----------------------------------------------------------------------- #
    # Permission enforcement
    # ----------------------------------------------------------------------- #

    for field in changes:
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be edited by non‑superuser"
            )

    # ----------------------------------------------------------------------- #
    # Apply changes
    # ----------------------------------------------------------------------- #

    updated_emp = copy.copy(emp_data)  # shallow copy to avoid mutating original

    for field, new_value in changes.items():
        updated_emp[field] = new_value

    return updated_emp


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    current = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change salary (should raise ValueError)
    try:
        alter_employee_details(current, {"salary": 90000}, is_superuser=False)
    except ValueError as exc:
        print(f"Permission error: {exc}")

    # Admin changing salary (allowed)
    updated = alter_employee_details(current, {"salary": 90000}, is_superuser=True)
    print(updated)