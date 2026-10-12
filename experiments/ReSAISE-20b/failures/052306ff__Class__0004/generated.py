import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary with the provided changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Mapping of field names to new values.
    is_superuser : bool
        True if the caller has admin privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If changes contain keys that the caller is not permitted to modify.
    """
    # Make a shallow copy to avoid mutating the original dict.
    updated = copy.deepcopy(emp_data)

    # Determine which keys are allowed to be changed.
    if is_superuser:
        allowed_keys = set(emp_data.keys())
    else:
        allowed_keys = EDITABLE_FIELDS & set(emp_data.keys())

    # Validate each change.
    for key, value in changes.items():
        if key not in allowed_keys:
            raise ValueError(
                f"User is not authorized to modify field '{key}'."
            )
        updated[key] = value

    return updated