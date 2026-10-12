from copy import deepcopy
from typing import Dict

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "salary",
    "department",
}

def update_employee_record(
    employee: Dict[str, any],
    updates: Dict[str, any],
    is_admin: bool,
) -> Dict[str, any]:
    """
    Update an employee record with the supplied changes.

    Parameters
    ----------
    employee : dict
        The original employee dictionary.
    updates : dict
        Dictionary of fields to be updated with new values.
    is_admin : bool
        If True, the caller has full privileges and may modify any field.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.

    Raises
    ------
    ValueError
        If updates contain keys that the caller is not allowed to modify.
    """
    # Create a shallow copy so the original employee dict is not mutated.
    updated = deepcopy(employee)

    # Determine which fields are allowed to be modified.
    if is_admin:
        allowed_fields = set(employee.keys())
    else:
        allowed_fields = EDITABLE_FIELDS

    # Validate and apply updates.
    for key, value in updates.items():
        if key not in allowed_fields:
            raise ValueError(
                f"User does not have permission to modify field '{key}'."
            )
        # Prevent accidental removal of required keys.
        if key not in employee:
            raise ValueError(f"Field '{key}' does not exist on the employee record.")
        updated[key] = value

    return updated