import copy

# Fields that regular users may edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

def adjust_employee_profile(emp: dict, changes: dict, has_admin_rights: bool) -> dict:
    """
    Update an employee's profile with the provided changes.

    Parameters
    ----------
    emp : dict
        The original employee record. Keys are attribute names.
    changes : dict
        Proposed modifications keyed by attribute name.
    has_admin_rights : bool
        If True, the caller may modify any field; otherwise only
        EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑editable field is attempted to be changed by a
        non‑admin, or if a requested change refers to an unknown
        attribute.
    """
    # Work on a copy to avoid mutating the original employee dict
    updated_emp = copy.deepcopy(emp)

    for key, new_value in changes.items():
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{key}' cannot be modified by a non‑admin user."
            )
        if key not in updated_emp:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")
        updated_emp[key] = new_value

    return updated_emp