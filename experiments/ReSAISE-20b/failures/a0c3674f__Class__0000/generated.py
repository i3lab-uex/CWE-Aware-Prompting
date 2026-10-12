import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee record with validated changes.

    Parameters
    ----------
    staff : dict
        Current state of the employee's details.
    changes : dict
        Desired key/value updates.
    admin_status : bool
        True if the updater has administrative privileges.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a restricted field.
    KeyError
        If the requested change refers to an unknown key in the staff record.

    Notes
    -----
    * The function never mutates its input arguments.
    * Sensitive fields (e.g., 'social_security_number') can only be modified by admins.
    """
    # Create a shallow copy to avoid mutating the original staff dict
    updated_staff = copy.deepcopy(staff)

    for field, new_value in changes.items():
        # Ensure the field exists in the original record
        if field not in staff:
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        # Non‑admin users may only modify EDITABLE_FIELDS
        if not admin_status and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff