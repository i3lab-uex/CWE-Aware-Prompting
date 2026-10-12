from copy import deepcopy
from typing import Dict, Any

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department", "salary"}

def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool
) -> Dict[str, Any]:
    """
    Update an employee record with the provided fields.

    Parameters
    ----------
    employee : dict
        Original employee data.  Keys may include: name, position,
        salary, department, social_security_number, etc.
    updates : dict
        Mapping of fields to new values.
    is_admin : bool
        Flag indicating if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a restricted field.
    KeyError
        If an update references a key that does not exist in the employee dict.
    TypeError
        If `updates` is not a mapping or contains non‑string keys.

    Notes
    -----
    - Only the fields listed in `EDITABLE_FIELDS` can be modified by regular users.
      The ``social_security_number`` field is reserved for admins only.
    - The function returns a *copy* of the employee dictionary; the original is left
      untouched.
    - The function performs shallow validation of update keys and values.  It does not
      attempt to validate value types beyond ensuring they are present.
    """
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Defensive copy of the original employee record
    updated_employee = deepcopy(employee)

    for key, value in updates.items():
        if not isinstance(key, str):
            raise TypeError(f"update key must be a string, got {type(key).__name__}")

        # Ensure the key exists in the original employee record
        if key not in employee:
            raise KeyError(f"Employee has no field named '{key}'")

        # Enforce access control
        if not is_admin:
            if key == "social_security_number":
                raise PermissionError("Only admins may modify social_security_number")
            if key not in EDITABLE_FIELDS:
                raise PermissionError(
                    f"Field '{key}' is not editable by regular users"
                )

        # Apply the update
        updated_employee[key] = value

    return updated_employee