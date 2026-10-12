from typing import Dict, Any

# Fields that regular users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other non-sensitive fields here.
}

class PermissionError(Exception):
    """Raised when a user attempts to modify restricted employee attributes."""
    pass

def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool
) -> Dict[str, Any]:
    """
    Update an employee's profile with the provided changes.

    Parameters
    ----------
    emp : dict
        Current employee data. Expected to contain keys like 'name',
        'position', 'salary', 'department', and 'social_security_number'.
    changes : dict
        Proposed modifications. Keys are attribute names to be updated.
    has_admin_rights : bool
        If True, the caller can modify any attribute. If False,
        only fields listed in EDITABLE_FIELDS are allowed.

    Returns
    -------
    dict
        The updated employee dictionary. A shallow copy is returned; the
        original `emp` dict remains unchanged.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a protected field.
    KeyError
        If a requested change refers to an attribute that does not exist in
        the employee record.
    """
    # Work on a copy to avoid mutating the original dictionary.
    updated_emp = emp.copy()

    for field, new_value in changes.items():
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Insufficient privileges to modify '{field}'. "
                "Only the following fields can be edited: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        if field not in updated_emp:
            raise KeyError(f"Employee record has no attribute '{field}'")

        # Perform the update
        updated_emp[field] = new_value

    return updated_emp