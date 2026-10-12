from copy import deepcopy
from typing import Dict

# Global set of fields that regular users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def update_employee_record(
    employee: Dict[str, any],
    updates: Dict[str, any],
    is_admin: bool
) -> Dict[str, any]:
    """
    Return a new employee dictionary with requested updates applied.

    Parameters
    ----------
    employee : dict
        Original employee record. Must contain keys:
            name, position, salary, department, social_security_number.
    updates : dict
        Mapping of fields to new values.
    is_admin : bool
        Flag indicating whether the caller has admin privileges.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    ValueError
        If an attempt is made to modify a protected field without admin rights,
        or if the updates contain keys that are not present in the original
        employee record.
    """
    # Defensive copy to avoid mutating input
    updated = deepcopy(employee)

    for field, new_value in updates.items():
        # Ensure the field exists on the employee record
        if field not in updated:
            raise ValueError(f"Field '{field}' does not exist on the employee record.")

        # Regular users can only modify editable fields
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify '{field}'. "
                "Only admins can change this field."
            )

        # Apply the update
        updated[field] = new_value

    return updated