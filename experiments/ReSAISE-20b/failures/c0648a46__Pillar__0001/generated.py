from typing import Dict, Any

# Global constant listing fields that can be edited by non‑admin users
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile with the provided changes.

    Parameters
    ----------
    worker : dict
        The current employee profile.
    changes : dict
        Mapping of fields to new values that should be applied.
    is_privileged : bool
        True if the caller has admin rights, False otherwise.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑privileged user attempts to modify a field that is not in
        EDITABLE_FIELDS.
    """
    # Work on a copy so the original dict remains unchanged until we are ready
    updated_profile = worker.copy()

    for field, new_value in changes.items():
        # Non‑admin users may only modify allowed fields
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be modified by a non‑privileged user."
            )
        # Apply the change
        updated_profile[field] = new_value

    return updated_profile