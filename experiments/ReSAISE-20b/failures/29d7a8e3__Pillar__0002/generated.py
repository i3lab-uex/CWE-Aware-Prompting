import copy

# Global constant listing fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is usually editable by managers, but we exclude it from non‑admin edits.
}

def edit_profile_data(profile: dict, modifications: dict, is_superuser: bool) -> dict:
    """
    Update an employee profile with the supplied modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile.
    modifications : dict
        Fields to modify and their new values.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a field that is not in
        ``EDITABLE_FIELDS`` or if any attempt is made to modify a protected
        field (e.g. ``social_security_number``) without superuser rights.
    """
    # Defensive copy to avoid mutating the original profile
    updated_profile = copy.deepcopy(profile)

    for field, new_value in modifications.items():
        # Protect sensitive fields that should only be changed by superusers
        if field == "social_security_number" and not is_superuser:
            raise ValueError("Modification of 'social_security_number' requires superuser privileges.")

        # Non‑admin users can only modify allowed fields
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(f"Field '{field}' is not editable by non‑admin users.")

        # Perform the update
        updated_profile[field] = new_value

    return updated_profile