# edit_personnel_info.py

"""
This module provides a single function, `edit_personnel_info`, which updates
employee records while respecting the permissions of the user performing
the update.

Author: ChatGPT
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the supplied adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Mapping of fields to new values that should be applied.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a non‑existent field or a field that
        the caller is not allowed to edit.
    """

    # Create a shallow copy so we don't mutate the original input
    updated_record = deepcopy(employee_record)

    for field, new_value in adjustments.items():
        # Field must exist in the original record
        if field not in employee_record:
            raise ValueError(f"Field '{field}' does not exist in the employee record.")

        # Non‑admin users can only edit fields listed in EDITABLE_FIELDS
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: non‑admin users cannot modify '{field}'."
            )

        # Perform the update
        updated_record[field] = new_value

    return updated_record


# ----------------- Unit tests (simple examples) -----------------
if __name__ == "__main__":
    # Sample employee record
    emp = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin updating salary and SSN
    admin_updates = {"salary": 95000, "social_security_number": "987-65-4321"}
    updated_emp = edit_personnel_info(emp, admin_updates, admin_flag=True)
    print("Admin update:", updated_emp)

    # Non‑admin attempting to change salary (should raise)
    try:
        edit_personnel_info(emp, {"salary": 95000}, admin_flag=False)
    except ValueError as e:
        print("Non‑admin error:", e)

    # Non‑admin updating allowed field
    updated_emp = edit_personnel_info(emp, {"department": "Research"}, admin_flag=False)
    print("Non‑admin update:", updated_emp)