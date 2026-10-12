from __future__ import annotations

# Fields that regular users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool = False
) -> dict:
    """
    Return a new dictionary with the employee data updated according to *alterations*.
    
    Parameters
    ----------
    worker : dict
        Current employee data. Must contain keys that correspond to the fields in *alterations*.
    alterations : dict
        Proposed changes. Keys must exist in *worker*; otherwise a ``KeyError`` is raised.
    admin_privileges : bool, optional
        If ``True``, all fields can be modified. Regular users may only modify the keys
        listed in ``EDITABLE_FIELDS``.
    
    Returns
    -------
    dict
        A new dictionary with the applied changes.
    
    Raises
    ------
    KeyError
        If an alteration refers to a field that does not exist in ``worker``.
    PermissionError
        If a regular user attempts to modify a non‑editable field.
    """
    # Validate that every key in alterations exists in the original worker dict
    missing = set(alterations) - set(worker)
    if missing:
        raise KeyError(f"Unknown field(s) in alterations: {', '.join(sorted(missing))}")

    # For non‑admin users, ensure only editable fields are changed
    if not admin_privileges:
        forbidden = set(alterations) - EDITABLE_FIELDS
        if forbidden:
            raise PermissionError(
                f"Insufficient privileges to modify: {', '.join(sorted(forbidden))}"
            )

    # Create a shallow copy to avoid mutating the original dict
    updated_worker = worker.copy()
    for key, value in alterations.items():
        updated_worker[key] = value

    return updated_worker