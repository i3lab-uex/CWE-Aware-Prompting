import copy

# Global list of fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(emp_data: dict, changes: dict, is_superuser: bool) -> dict:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of an employee record.
    changes : dict
        Mapping of field names to new values.
    is_superuser : bool
        Flag indicating whether the caller has admin privileges.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    ValueError
        If a change references an unknown field or a non‑admin attempts to modify a protected field.
    """
    # Validate input types
    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")
    if not isinstance(is_superuser, bool):
        raise TypeError("is_superuser must be a boolean")

    # Create a shallow copy to avoid mutating the original
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        # Reject unknown fields
        if field not in emp_data:
            raise ValueError(f"Unknown field '{field}' cannot be updated")

        # Enforce non‑admin restrictions
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the '{field}' field"
            )

        # Apply the change
        updated[field] = new_value

    return updated