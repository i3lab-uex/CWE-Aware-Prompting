# Global set of fields that can be edited by regular users
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_data(worker: dict, alterations: dict, admin_privileges: bool) -> dict:
    """
    Update an employee dictionary with the provided alterations.

    Parameters
    ----------
    worker : dict
        The original employee data. Expected keys include at least:
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.
    alterations : dict
        A mapping of attribute names to the new values that should be applied.
    admin_privileges : bool
        If ``True`` the caller has full edit rights.  Otherwise only fields
        listed in :data:`EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``worker`` dictionary is left untouched.

    Raises
    ------
    KeyError
        If an alteration refers to a key that does not exist in ``worker``.
    PermissionError
        If a non‑admin attempts to modify a field not in :data:`EDITABLE_FIELDS`.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(admin_privileges, bool):
        raise TypeError("admin_privileges must be a boolean")

    # Work on a copy so that the original is not mutated
    updated = worker.copy()

    for field, new_value in alterations.items():
        if field not in updated:
            raise KeyError(f"Field '{field}' does not exist in the employee record")

        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Insufficient privileges to modify '{field}'. "
                "Only the following fields may be edited: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        updated[field] = new_value

    return updated