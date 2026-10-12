# Global list of fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(emp_data: dict, changes: dict, is_superuser: bool) -> dict:
    """
    Update an employee's details with the provided changes.

    Parameters
    ----------
    emp_data : dict
        Current employee record.
    changes : dict
        Proposed updates (field -> new value).
    is_superuser : bool
        True if the updater has admin privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field outside EDITABLE_FIELDS.
    TypeError
        If emp_data or changes is not a mapping type.
    """
    if not isinstance(emp_data, dict) or not isinstance(changes, dict):
        raise TypeError("emp_data and changes must be dictionaries")

    # Create a shallow copy to avoid mutating the original input
    updated = emp_data.copy()

    for field, new_value in changes.items():
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be modified by a non‑admin user."
            )
        # Perform the update
        updated[field] = new_value

    return updated