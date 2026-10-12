#!/usr/bin/env python3
"""
Employee data modification module.

Provides a single public function, `modify_employee_data`, which updates an
employee dictionary according to supplied alterations while enforcing
privilege checks and field restrictions.

The module is intentionally minimal, avoiding external dependencies.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

#: Fields that regular users are allowed to edit.  All other fields require
#: administrative privileges.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Update an employee dictionary with the given alterations.

    Parameters
    ----------
    worker : dict
        The original employee data.  Keys may include any of the following:
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    alterations : dict
        A mapping of keys to new values that should be applied to the employee.
    admin_privileges : bool
        ``True`` if the caller has administrative rights.  When ``False``
        only keys present in :data:`EDITABLE_FIELDS` may be modified.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``worker`` is not modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not listed in
        :data:`EDITABLE_FIELDS`, or if an alteration references a key that does
        not exist in ``worker``.
    """
    # Create a shallow copy to avoid mutating the input dictionary
    updated_worker = copy.deepcopy(worker)

    # Validate alterations
    for key, new_value in alterations.items():
        if key not in worker:
            raise ValueError(f"Unknown field '{key}' cannot be modified.")

        if not admin_privileges and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field '{key}'. "
                "Only {EDITABLE_FIELDS} are editable for regular users."
            )

        # Perform the update
        updated_worker[key] = new_value

    return updated_worker


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Engineer", "salary": 95000}

    # Admin user
    print(modify_employee_data(employee, changes, admin_privileges=True))

    # Regular user (should raise an exception for 'salary')
    try:
        print(modify_employee_data(employee, changes, admin_privileges=False))
    except ValueError as exc:
        print(f"Permission error: {exc}")