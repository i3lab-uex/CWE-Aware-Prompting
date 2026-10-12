#!/usr/bin/env python3
"""
Employee data modification module.

The function `modify_employee_data` updates an employee dictionary with the
specified alterations while enforcing access controls.  Regular users may only
modify attributes listed in `EDITABLE_FIELDS`.  Administrators are exempt from
this restriction and may modify any attribute.

The implementation follows best practices to mitigate CWE‑915 by ensuring
that only explicitly permitted attributes are altered, regardless of the
content of the `alterations` dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Global set of fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Add other non‑sensitive fields here.
}


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
        Dictionary representing an employee.  Expected keys include:
        ``name``, ``position``, ``salary``, ``department``,
        ``social_security_number`` and possibly others.
    alterations : dict
        Proposed modifications.  Keys are attribute names, values are the new
        values to assign.
    admin_privileges : bool
        ``True`` if the caller has administrative rights; otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``worker`` is not modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    """
    # Create a shallow copy to avoid mutating the original dictionary.
    updated_worker = copy.deepcopy(worker)

    # Iterate over requested alterations and enforce access control.
    for key, value in alterations.items():
        if not admin_privileges:
            if key not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Unauthorized modification of field '{key}'. "
                    "Only editable fields are allowed."
                )
        # Perform the update.
        updated_worker[key] = value

    return updated_worker