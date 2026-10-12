import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee record reflecting the requested changes.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Key/value pairs with fields to be updated.
    is_superuser : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field.
    """
    # Work on a shallow copy to avoid mutating the original dictionary
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        # Skip unknown fields silently
        if field not in updated:
            continue

        # Non‑admins may only edit allowed fields
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify '{field}'. "
                "Only the following fields may be edited: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        # Apply the change
        updated[field] = new_value

    return updated