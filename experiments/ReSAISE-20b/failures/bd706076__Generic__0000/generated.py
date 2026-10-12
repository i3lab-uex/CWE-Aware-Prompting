# update_employee_record.py

from copy import deepcopy
from typing import Dict, Any

# Fields that regular users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool
) -> Dict[str, Any]:
    """
    Update an employee record with the given updates.

    Parameters
    ----------
    employee : dict
        Original employee dictionary. Must contain keys like
        'name', 'position', 'salary', 'department',
        and optionally sensitive fields such as
        'social_security_number'.
    updates : dict
        Dictionary of field names to new values.
    is_admin : bool
        If True, the caller has administrative privileges and can update any field.
        If False, only fields listed in EDITABLE_FIELDS may be updated.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If `updates` contains a key that does not exist in the employee record.
    PermissionError
        If a non‑admin attempts to update a field not in EDITABLE_FIELDS.
    """
    # Ensure we do not modify the original employee dict
    updated = deepcopy(employee)

    for field, new_value in updates.items():
        if field not in employee:
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        if not is_admin and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the '{field}' field."
            )

        # Basic type validation could be added here if needed
        updated[field] = new_value

    return updated