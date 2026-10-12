from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}

def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return a new employee record with the requested adjustments applied.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key‑value pairs for fields and their new data.
    admin_flag : bool
        True if the requester has administrative privileges.

    Returns
    -------
    dict
        Updated employee record reflecting valid changes.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a protected field or if
        the field does not exist in the record.
    """
    # Make a defensive copy to avoid mutating the original
    updated_record = deepcopy(employee_record)

    # Determine which fields are permissible to edit
    allowed_fields = (
        set(updated_record.keys()) if admin_flag else EDITABLE_FIELDS & set(updated_record.keys())
    )

    for field, new_value in adjustments.items():
        if field not in updated_record:
            raise ValueError(f"Field '{field}' does not exist in the employee record.")
        if field not in allowed_fields:
            raise ValueError(f"Insufficient permissions to modify '{field}'.")
        # Perform a shallow type check (optional but helps catch obvious mistakes)
        if isinstance(updated_record[field], int) and not isinstance(new_value, int):
            raise ValueError(f"Field '{field}' expects an integer value.")
        if isinstance(updated_record[field], str) and not isinstance(new_value, str):
            raise ValueError(f"Field '{field}' expects a string value.")
        updated_record[field] = new_value

    return updated_record