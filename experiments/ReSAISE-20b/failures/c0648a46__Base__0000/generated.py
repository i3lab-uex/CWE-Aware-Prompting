import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker : dict
        Current employee profile.
    changes : dict
        Mapping of field names to new values.
    is_privileged : bool
        True if the caller has administrative privileges.

    Raises
    ------
    ValueError
        If a non‑privileged caller attempts to modify a disallowed field.
    KeyError
        If the requested field does not exist in the profile.

    Returns
    -------
    dict
        The updated employee profile.
    """
    # Work on a shallow copy to avoid mutating the original
    updated = copy.deepcopy(worker)

    for field, new_value in changes.items():
        # Ensure the field exists in the profile
        if field not in updated:
            raise KeyError(f"Field '{field}' does not exist in the employee profile.")

        # Check permissions
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑privileged users cannot modify the field '{field}'."
            )

        # Apply the change
        updated[field] = new_value

    return updated