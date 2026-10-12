#!/usr/bin/env python3
"""
Utility to generate a formatted employee directory for a specific department.

The function inspects the supplied template string, ensures that only
non‑sensitive employee attributes are referenced, and then substitutes those
attributes for every employee belonging to the requested department.
"""

from __future__ import annotations

import sys
import traceback
from dataclasses import dataclass, fields
from string import Formatter
from typing import Iterable

# --------------------------------------------------------------------------- #
# 1. Employee model (this would normally be imported from your application)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Simple employee representation."""
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# --------------------------------------------------------------------------- #
# 2. Global employee collection (replace with real data source)
# --------------------------------------------------------------------------- #

# In a real application this would be replaced by a database query or an API call.
EMPLOYEES: Iterable[Employee] = (
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Product Manager", "Product", 105000.0, "bob.johnson@company.com"),
    Employee("Carol Lee", "Designer", "Design", 78000.0, "carol.lee@company.com"),
    Employee("David Kim", "Software Engineer", "Engineering", 92000.0, "david.kim@company.com"),
)

# --------------------------------------------------------------------------- #
# 3. Helper utilities
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"salary", "personal_email"}


def _validate_template(template: str) -> None:
    """
    Ensure that the template only references non‑sensitive employee attributes.
    Raises ValueError if a sensitive field is detected or an invalid placeholder
    is found.
    """
    formatter = Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if not field_name:
            continue  # Skip empty fields
        parts = field_name.split(".")
        if len(parts) != 2 or parts[0] != "employee":
            raise ValueError(f"Invalid placeholder '{field_name}'. Expected format '{{{{employee.<attribute>}}}}'")
        attr = parts[1]
        if attr in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed.")
        # Ensure the attribute actually exists on Employee
        if attr not in {f.name for f in fields(Employee)}:
            raise ValueError(f"Employee has no attribute '{attr}'.")


def _format_employee(employee: Employee, template: str) -> str:
    """
    Return the template string with placeholders replaced by values from
    `employee`. Only non‑sensitive attributes are used.
    """
    # Build a mapping of allowed attributes
    attr_map = {f.name: getattr(employee, f.name) for f in fields(Employee) if f.name not in _SENSITIVE_FIELDS}
    try:
        return template.format(employee=attr_map)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format template for employee '{employee.name}': {exc}") from exc


# --------------------------------------------------------------------------- #
# 4. Main API
# --------------------------------------------------------------------------- #

def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory string for all employees in `dept_name`.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as `{employee.name}` or
        `{employee.position}`.  Sensitive attributes (salary, personal_email)
        are prohibited.

    Returns
    -------
    str
        The concatenated directory entries for all matching employees, each on
        a separate line.

    Raises
    ------
    ValueError
        If the template references sensitive data, contains invalid placeholders,
        or any other error occurs during processing.
    """
    try:
        # Validate the template once
        _validate_template(dir_template)

        # Filter employees by department (case‑insensitive)
        matching = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
        if not matching:
            return f"No employees found in department '{dept_name}'."

        # Format each employee
        formatted_entries = [_format_employee(emp, dir_template) for emp in matching]
        return "\n".join(formatted_entries)

    except Exception as exc:
        # Log the full traceback for debugging (optional)
        sys.stderr.write(f"Error generating directory: {exc}\n")
        traceback.print_exc(file=sys.stderr)
        raise ValueError(f"Failed to generate department directory: {exc}") from exc


# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_department_directory("Engineering", template))