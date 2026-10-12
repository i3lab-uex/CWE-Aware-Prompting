# Global constant defining which fields a non‑admin user may modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def adjust_employee_details(person: dict,
                            alterations: dict,
                            has_admin_rights: bool) -> dict:
    """
    Return an updated employee profile after applying the requested alterations.

    Parameters
    ----------
    person : dict
        Current employee profile.
    alterations : dict
        Mapping of fields to new values that should be applied.
    has_admin_rights : bool
        If True, all fields can be updated; otherwise only those listed in
        ``EDITABLE_FIELDS`` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a field not listed in
        ``EDITABLE_FIELDS``.
    KeyError
        If an alteration refers to a field that does not exist in the original
        profile.
    """
    # Make a shallow copy so we do not mutate the caller's dictionary
    updated = person.copy()

    for field, new_value in alterations.items():
        # Ensure the field exists in the original profile
        if field not in person:
            raise KeyError(f"Field '{field}' does not exist in the employee profile.")

        # Enforce permission checks
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated[field] = new_value

    return updated