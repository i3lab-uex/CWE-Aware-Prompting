import copy

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

class UnauthorizedFieldError(RuntimeError):
    """Raised when a non‑admin user attempts to modify a protected field."""
    pass

def adjust_employee_details(person: dict, alterations: dict, has_admin_rights: bool) -> dict:
    """
    Update an employee profile with the given alterations.

    Parameters
    ----------
    person : dict
        Current employee profile.  Keys may include 'name', 'position',
        'salary', 'department', and 'social_security_number'.
    alterations : dict
        Fields to be updated with new values.
    has_admin_rights : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The original
        ``person`` dictionary is left untouched.

    Raises
    ------
    UnauthorizedFieldError
        If a non‑admin attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    """
    # Work on a shallow copy to avoid mutating the original dict.
    updated = copy.deepcopy(person)

    for field, new_value in alterations.items():
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise UnauthorizedFieldError(
                f"Non‑admin users cannot modify the field '{field}'."
            )
        updated[field] = new_value

    return updated