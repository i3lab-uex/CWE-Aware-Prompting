from typing import Dict, Set

# Global set of fields that regular users are allowed to edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

def modify_staff_details(
    employee_data: Dict[str, any],
    changes: Dict[str, any],
    is_superuser: bool
) -> Dict[str, any]:
    """
    Apply a set of changes to an employee record.

    Parameters
    ----------
    employee_data : dict
        The original employee dictionary.
    changes : dict
        Proposed modifications keyed by attribute name.
    is_superuser : bool
        True if the caller has admin privileges.

    Returns
    -------
    dict
        The updated employee dictionary (a shallow copy).

    Raises
    ------
    ValueError
        If a regular user attempts to modify a non‑editable field.
    TypeError
        If `employee_data` or `changes` is not a mapping type.
    """
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Work on a copy to avoid side‑effects.
    updated = employee_data.copy()

    for field, new_value in changes.items():
        # Validate that the field exists in the employee record.
        if field not in employee_data:
            raise ValueError(f"Field '{field}' does not exist on the employee record")

        if not is_superuser:
            # Non‑superusers may only modify predefined fields.
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Regular users cannot modify the field '{field}'. "
                    "Only {EDITABLE_FIELDS} are editable."
                )
        # Apply the change.
        updated[field] = new_value

    return updated