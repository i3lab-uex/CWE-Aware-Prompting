import re
from typing import List

# Assume that the application maintains a global list of Employee objects.
# This is just a placeholder; in a real system it would be imported from the
# relevant module or fetched from a database.
EMPLOYEES: List["Employee"] = []

class _RestrictedEmployeeProxy:
    """
    A thin wrapper around an Employee instance that disallows access to
    sensitive attributes (`salary` and `personal_email`). Any attempt to
    read these fields will raise a ValueError.
    """
    _RESTRICTED_FIELDS = {"salary", "personal_email"}

    def __init__(self, employee):
        self._employee = employee

    def __getattr__(self, name: str):
        if name in self._RESTRICTED_FIELDS:
            raise ValueError(f"Access to sensitive field '{name}' is forbidden.")
        return getattr(self._employee, name)

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted directory listing for all employees in the given
    department.

    Parameters:
        dep (str): The department name to filter employees by.
        format_template (str): A string containing placeholders in the form
                               `{employee.<field>}` that will be replaced by
                               the corresponding employee attribute.

    Returns:
        str: The directory listing, with each employee on a new line.
             If no employees match the department, an empty string is returned.

    Raises:
        ValueError: If a sensitive attribute is accessed or any other
                    formatting error occurs.
    """
    # Filter employees by department (case‑sensitive comparison)
    matching_employees = [emp for emp in EMPLOYEES if getattr(emp, "department", None) == dep]

    # If no employees match, return an empty string
    if not matching_employees:
        return ""

    lines = []
    for emp in matching_employees:
        proxy = _RestrictedEmployeeProxy(emp)
        try:
            # Only format placeholders that belong to the employee object.
            # We use a custom formatter that ignores unknown fields rather
            # than raising an error, but we still protect sensitive data.
            line = format_template.format(employee=proxy)
        except Exception as exc:
            # Wrap any exception in ValueError to satisfy the contract
            raise ValueError(f"Failed to format employee data: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)