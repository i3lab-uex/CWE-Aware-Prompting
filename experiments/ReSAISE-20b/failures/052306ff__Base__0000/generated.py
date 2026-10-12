import copy
from typing import Dict, Any

# Fields that regular users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with validated changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee record.
    changes : dict
        Desired updates. Keys are attribute names, values are new data.
    is_superuser : bool
        If True, the caller has permission to modify any field.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a restricted field.
    KeyError
        If the employee dictionary does not contain a requested key (ensuring
        we don't silently create new keys).
    """
    # Make a shallow copy to avoid mutating the original dict.
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        # Ensure the field exists in the original record.
        if field not in emp_data:
            raise KeyError(f"Field '{field}' does not exist in employee data.")

        # Check permission.
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify '{field}' "
                "without superuser privileges."
            )

        # Apply the change.
        updated[field] = new_value

    return updated