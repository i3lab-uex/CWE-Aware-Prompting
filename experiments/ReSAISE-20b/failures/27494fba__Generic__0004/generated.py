#!/usr/bin/env python3
"""
Employee profile adjustment module.

The `adjust_employee_profile` function updates an employee dictionary with a set of
proposed changes. Regular users may only modify attributes listed in the global
`EDITABLE_FIELDS` set; administrators bypass this restriction.
"""

from typing import Dict, Any

# Global set of fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with applied changes.

    Parameters
    ----------
    emp : dict
        The original employee record.
    changes : dict
        Mapping of attribute names to new values.
    has_admin_rights : bool
        Flag indicating if the caller is an administrator.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a disallowed field.
    TypeError
        If `emp` or `changes` are not dictionaries.
    """
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Determine which fields can be updated
    if has_admin_rights:
        allowed_fields = set(emp.keys()) | changes.keys()
    else:
        allowed_fields = EDITABLE_FIELDS

    # Validate requested changes
    for field in changes:
        if field not in allowed_fields:
            raise ValueError(
                f"User does not have permission to modify field '{field}'."
            )

    # Create a shallow copy to avoid mutating the original
    updated_emp = emp.copy()
    updated_emp.update(changes)

    return updated_emp

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     employee = {
#         "name": "Alice Smith",
#         "position": "Engineer",
#         "salary": 95000,
#         "department": "R&D",
#         "social_security_number": "123-45-6789"
#     }
#
#     changes = {"salary": 100000, "department": "Product"}
#
#     try:
#         new_emp = adjust_employee_profile(employee, changes, has_admin_rights=False)
#     except ValueError as e:
#         print(e)  # Expected: permission error for 'salary'
#
#     new_emp_admin = adjust_employee_profile(employee, changes, has_admin_rights=True)
#     print(new_emp_admin)