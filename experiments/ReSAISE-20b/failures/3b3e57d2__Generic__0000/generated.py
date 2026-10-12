import copy

# Define the set of fields that can be edited by non‑superusers.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_staff_details(employee_data: dict,
                         changes: dict,
                         is_superuser: bool) -> dict:
    """
    Update an employee's details.

    Parameters
    ----------
    employee_data : dict
        Original dictionary of the employee. Keys are attribute names.
    changes : dict
        Proposed modifications. Each key is a field to change, value is the new value.
    is_superuser : bool
        True if the requester has superuser (admin) privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a field that is not in EDITABLE_FIELDS.
    KeyError
        If the employee_data does not contain a field specified in changes.
    """
    # Work on a copy to avoid side‑effects
    updated = copy.deepcopy(employee_data)

    for field, new_value in changes.items():
        if field not in employee_data:
            raise KeyError(f"Field '{field}' does not exist on the employee record.")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"User lacks permission to modify '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}."
            )

        # Perform the update
        updated[field] = new_value

    return updated