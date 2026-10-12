from __future__ import annotations

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return a new profile dictionary with the requested modifications applied.

    Parameters
    ----------
    profile : dict
        Current employee profile.
    modifications : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        If True, the caller has admin privileges and may modify any field.
        Otherwise only fields listed in ``EDITABLE_FIELDS`` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a field that is not in
        ``EDITABLE_FIELDS`` or if the modification references a key
        that does not exist in the original profile.
    """
    # Make a shallow copy so we don't mutate the input dictionary.
    updated_profile = profile.copy()

    for key, new_value in modifications.items():
        if key not in profile:
            raise ValueError(f"Field '{key}' does not exist in the profile.")

        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

        updated_profile[key] = new_value

    return updated_profile