#!/usr/bin/env python3
"""
Secure staff details modification utility.

The function `modify_staff_details` updates an employee dictionary while
respecting role‑based restrictions on which fields may be altered by a
regular user.  Superusers (admins) are exempt from these restrictions.

Security Note:
- Only the keys present in `employee_data` may be updated.
- The function performs a shallow copy of the input dictionary to avoid
  mutating callers' data in place.
- No dynamic code execution or attribute access beyond dictionary operations
  is performed, mitigating CWE‑913 risks.
"""

from copy import deepcopy
from typing import Dict

# Global set of fields that a non‑superuser is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_staff_details(
    employee_data: Dict[str, any],
    changes: Dict[str, any],
    is_superuser: bool
) -> Dict[str, any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    employee_data : dict
        The original employee record.
    changes : dict
        Proposed modifications; keys are attribute names, values are new values.
    is_superuser : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a protected field.
    """
    # Create a shallow copy to avoid mutating the original data
    updated = deepcopy(employee_data)

    for key, new_value in changes.items():
        # Only allow updates to existing fields
        if key not in employee_data:
            continue  # silently ignore unknown keys

        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Unauthorized modification attempt of field '{key}' "
                "by a non‑superuser."
            )

        updated[key] = new_value

    return updated