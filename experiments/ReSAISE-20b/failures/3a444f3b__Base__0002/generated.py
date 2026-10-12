import copy

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def edit_personnel_info(employee_record: dict, adjustments: dict, admin_flag: bool) -> dict:
    """
    Update an employee record with the provided adjustments.

    Parameters
    ----------
    employee_record : dict
        The current state of an employee's details.
    adjustments : dict
        Keys are the fields to update, values are the new data.
    admin_flag : bool
        True if the updater has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a disallowed field or a non‑existent key.
    """
    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")
    if not isinstance(admin_flag, bool):
        raise TypeError("admin_flag must be a boolean")

    # Create a shallow copy to avoid mutating the original record
    updated_record = copy.deepcopy(employee_record)

    # Determine which fields are allowed to be changed
    if admin_flag:
        allowed_fields = set(employee_record.keys())
    else:
        # Non‑admin can only modify a subset
        allowed_fields = EDITABLE_FIELDS & set(employee_record.keys())

    for key, new_value in adjustments.items():
        if key not in employee_record:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")
        if key not in allowed_fields:
            raise ValueError(f"Modification of field '{key}' is not permitted.")
        updated_record[key] = new_value

    return updated_record