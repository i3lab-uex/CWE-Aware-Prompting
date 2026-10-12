import copy

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other safe fields here
}

def modify_employee_profile(worker: dict, changes: dict, is_privileged: bool) -> dict:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker : dict
        The current employee profile.
    changes : dict
        Mapping of field names to new values that should be applied.
    is_privileged : bool
        If True, the caller has admin rights and can modify any field.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify a field that is not in
        ``EDITABLE_FIELDS`` or if an invalid key/value pair is supplied.
    """
    # Validate input types
    if not isinstance(worker, dict):
        raise ValueError("worker must be a dictionary")
    if not isinstance(changes, dict):
        raise ValueError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original profile
    updated = copy.deepcopy(worker)

    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise ValueError(f"Field name must be a string: {field!r}")

        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑privileged users cannot modify the field: {field}"
            )

        # Apply the change
        updated[field] = new_value

    return updated