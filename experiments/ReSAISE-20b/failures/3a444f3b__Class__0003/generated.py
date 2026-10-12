# Global list of fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def edit_personnel_info(employee_record: dict,
                        adjustments: dict,
                        admin_flag: bool) -> dict:
    """
    Return a new employee record with allowed modifications applied.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Mapping of fields to new values.
    admin_flag : bool
        ``True`` if the updater is an administrator.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If ``employee_record`` is not a dictionary.
    """

    if not isinstance(employee_record, dict):
        raise ValueError("employee_record must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_record = employee_record.copy()

    # Determine which fields are allowed to be edited
    allowed_fields = set(employee_record.keys())
    if not admin_flag:
        # Non‑admin users may only edit fields in EDITABLE_FIELDS
        allowed_fields.intersection_update(EDITABLE_FIELDS)

    # Apply adjustments only if the field is permitted
    for key, value in adjustments.items():
        if key in allowed_fields:
            updated_record[key] = value
        else:
            # For security we silently ignore disallowed keys.
            # Alternatively, raise an exception if strict enforcement is required.
            pass

    return updated_record