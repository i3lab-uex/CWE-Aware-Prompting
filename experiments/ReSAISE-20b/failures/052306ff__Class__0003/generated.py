# Global list of fields that non-superusers are allowed to edit.
EDITABLE_FIELDS = ["name", "position", "department"]

def alter_employee_details(emp_data: dict, changes: dict, is_superuser: bool) -> dict:
    """
    Return a new employee dictionary with validated changes applied.

    Parameters
    ----------
    emp_data : dict
        The current employee record.
    changes : dict
        Keys are field names, values are the new data to set.
    is_superuser : bool
        If True, all fields may be updated.  If False, only those in
        EDITABLE_FIELDS may be changed.

    Returns
    -------
    dict
        A new dictionary with the updates applied.

    Raises
    ------
    ValueError
        If a non-superuser attempts to modify a restricted field.
    """
    # Create a shallow copy so we don't mutate the original dictionary
    updated = emp_data.copy()

    for field, new_value in changes.items():
        # Validate that the field exists in the employee record
        if field not in emp_data:
            raise ValueError(f"Field '{field}' does not exist in employee data.")

        # Non-superusers are limited to EDITABLE_FIELDS
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(f"Insufficient permissions to modify '{field}'.")

        # Apply the change
        updated[field] = new_value

    return updated