import copy

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

def alter_employee_details(emp_data: dict, changes: dict, is_superuser: bool) -> dict:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp_data : dict
        Current employee record.
    changes : dict
        Mapping of field names to new values.
    is_superuser : bool
        Flag indicating whether the updater has admin rights.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    KeyError
        If a change refers to a field that does not exist in ``emp_data``.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    """
    # Make a shallow copy so the original data is not mutated
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        # Ensure the field exists
        if field not in updated:
            raise KeyError(f"Field '{field}' does not exist in employee record.")

        # Non‑admin users can only modify fields listed in EDITABLE_FIELDS
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated[field] = new_value

    return updated