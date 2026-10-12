#!/usr/bin/env python3
"""
Utility to safely modify employee data.

The module defines a single public function `modify_employee_data` that
updates an employee dictionary while enforcing field‑level permissions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Set


# Global set of fields that a non‑admin user may edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}


class UnauthorizedFieldModificationError(RuntimeError):
    """Raised when an attempt is made to modify a protected field without admin rights."""
    pass


def _validate_alterations(
    alterations: Dict[str, any], admin_privileges: bool
) -> None:
    """
    Validate that the requested alterations are allowed.

    Parameters
    ----------
    alterations : dict
        Mapping of field names to new values.
    admin_privileges : bool
        Whether the caller has administrative privileges.

    Raises
    ------
    UnauthorizedFieldModificationError
        If a non‑admin attempts to modify a field outside EDITABLE_FIELDS.
    """
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")

    if admin_privileges:
        # Admins can modify any field; no further checks required.
        return

    disallowed = set(alterations) - EDITABLE_FIELDS
    if disallowed:
        raise UnauthorizedFieldModificationError(
            f"Non‑admin users cannot modify fields: {', '.join(sorted(disallowed))}"
        )


def modify_employee_data(
    worker: Dict[str, any],
    alterations: Dict[str, any],
    admin_privileges: bool,
) -> Dict[str, any]:
    """
    Safely modify an employee's details.

    Parameters
    ----------
    worker : dict
        Current state of the employee record. Expected keys include:
            - name (str)
            - position (str)
            - salary (int/float)
            - department (str)
            - social_security_number (str)
    alterations : dict
        Proposed changes mapping field names to new values.
    admin_privileges : bool
        ``True`` if the caller is an administrator; otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    UnauthorizedFieldModificationError
        If a non‑admin attempts to modify a protected field.
    TypeError
        If the inputs are not of the expected types.

    Notes
    -----
    * The original ``worker`` dictionary is **not** modified; a deep copy
      is returned instead.  This protects callers from accidental side‑effects.
    * The function only validates that the keys in ``alterations`` are
      permitted.  It does not perform type checks on individual values.
    """
    # Basic type validation
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")

    # Enforce field‑level permissions
    _validate_alterations(alterations, admin_privileges)

    # Create a deep copy to avoid mutating the caller's data
    updated_worker = deepcopy(worker)

    # Apply changes
    for key, value in alterations.items():
        updated_worker[key] = value

    return updated_worker


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     employee = {
#         "name": "Alice Smith",
#         "position": "Engineer",
#         "salary": 90000,
#         "department": "R&D",
#         "social_security_number": "123-45-6789"
#     }
#
#     changes = {"salary": 95000, "department": "Engineering"}
#
#     try:
#         updated = modify_employee_data(employee, changes, admin_privileges=False)
#         print(updated)
#     except UnauthorizedFieldModificationError as e:
#         print(f"Permission error: {e}")