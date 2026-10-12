import copy
from typing import Dict, Any

# Global constant: fields that non‑admin users are allowed to modify
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # add other safe fields here
}

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Update an employee profile with the supplied modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile. Must be a mapping of field names to values.
    modifications : dict
        Desired updates; keys are the fields to change, values are the new values.
    is_superuser : bool
        If True, all fields may be updated; otherwise only those in EDITABLE_FIELDS.

    Returns
    -------
    dict
        A new dictionary containing the updated profile. The original `profile`
        is left untouched.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a field that is not in
        `EDITABLE_FIELDS`, or if any key in `modifications` is not a string.
    """
    # Defensive copy to avoid mutating the caller's dictionary
    updated_profile = copy.deepcopy(profile)

    for field, new_value in modifications.items():
        if not isinstance(field, str):
            raise ValueError(f"Field name must be a string; got {field!r}")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Unauthorized modification of field '{field}'. "
                "Only the following fields are editable: "
                f"{sorted(EDITABLE_FIELDS)}"
            )

        # Perform the update
        updated_profile[field] = new_value

    return updated_profile