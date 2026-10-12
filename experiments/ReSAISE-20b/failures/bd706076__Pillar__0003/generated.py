from copy import deepcopy
from typing import Dict, Any

# Fields that can be updated by non‑admin users
EDITABLE_FIELDS = {"name", "position", "department"}

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the supplied changes.

    Parameters
    ----------
    employee : dict
        Original employee data. Keys may include sensitive fields such as
        'social_security_number' and 'salary'.
    updates : dict
        Fields to be updated with their new values.
    is_admin : bool
        If True, all fields may be updated.  If False, only keys in
        EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If ``updates`` is not a dictionary.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    KeyError
        If ``updates`` contains a key that is not present in the original
        employee record.
    """
    if not isinstance(updates, dict):
        raise ValueError("updates must be a dictionary")

    # Make a deep copy to avoid mutating the original employee dict
    updated = deepcopy(employee)

    for key, value in updates.items():
        # Ensure the field exists on the employee record
        if key not in updated:
            raise KeyError(f"Field '{key}' does not exist on the employee record")

        # Non‑admin users can only modify allowed fields
        if not is_admin and key not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

        # Apply the update
        updated[key] = value

    return updated