import copy

# Fields that a non‑superuser is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_staff_details(employee_data: dict,
                         changes: dict,
                         is_superuser: bool) -> dict:
    """
    Return an updated employee dictionary after applying the requested changes.

    Parameters
    ----------
    employee_data : dict
        Current data of an employee.
    changes : dict
        Proposed modifications (field → new value).
    is_superuser : bool
        ``True`` if the caller has admin privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a regular user attempts to modify a non‑editable field.
    """
    # Work on a copy so the original dictionary is never mutated.
    updated = copy.deepcopy(employee_data)

    for field, new_value in changes.items():
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify '{field}' for non‑superuser"
            )
        # Allow updates only if the field exists in the original data.
        # If a new field is supplied, superusers can add it; others cannot.
        if field in employee_data or is_superuser:
            updated[field] = new_value

    return updated