import copy

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


def modify_staff_info(staff: dict, changes: dict, admin_status: bool) -> dict:
    """
    Return a new employee dictionary with validated updates applied.

    Parameters
    ----------
    staff : dict
        Current state of the employee record.
    changes : dict
        Desired field updates. Keys are attribute names, values are new data.
    admin_status : bool
        True if the caller is an administrator.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field or if a key does not exist in the
        original record.
    """
    # Create a shallow copy so we don't mutate the caller's dict
    updated = copy.deepcopy(staff)

    for key, new_value in changes.items():
        # Reject unknown keys
        if key not in staff:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")

        # Non‑admin users can only modify a limited set of fields
        if not admin_status and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users are not permitted to modify the '{key}' field."
            )

        # Apply the change
        updated[key] = new_value

    return updated