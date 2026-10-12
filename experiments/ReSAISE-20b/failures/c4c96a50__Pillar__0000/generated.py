#!/usr/bin/env python3
"""
Employee directory assembler.

The module defines:
- `assemble_employee_list(dept_name: str, template: str) -> str`
  Builds a formatted employee directory for the specified department
  using a template that may contain placeholders such as
  `{employee.name}` or `{employee.position}`.

The implementation protects against accessing restricted fields
(`salary`, `personal_email`). If such an attempt is detected, a
`ValueError` is raised.

The module also contains minimal `Employee` and `EMPLOYEES`
definitions for demonstration purposes. In a real application these
would be imported from the appropriate data layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


# ----------------------------------------------------------------------
# Demo data model (replace with real imports in production)
# ----------------------------------------------------------------------


@dataclass
class Employee:
    """Simple employee data container."""
    name: str
    position: str
    department: str
    salary: float = field(repr=False)
    personal_email: str = field(repr=False)


# Example employee database
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering",
             salary=95000.0, personal_email="alice.smith@example.com"),
    Employee("Bob Johnson", "Senior Analyst", "Finance",
             salary=88000.0, personal_email="bob.johnson@example.com"),
    Employee("Carol Williams", "HR Manager", "Human Resources",
             salary=77000.0, personal_email="carol.williams@example.com"),
    # ... add more employees as needed
]


# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------


class _SafeEmployeeProxy:
    """
    Proxy object that exposes only allowed attributes of an Employee.
    Attempts to access restricted fields raise ValueError.
    """

    _ALLOWED_ATTRS = {"name", "position", "department"}

    def __init__(self, employee: Employee) -> None:
        self._employee = employee

    def __getattr__(self, name: str):
        if name not in self._ALLOWED_ATTRS:
            raise ValueError(
                f"Access to restricted attribute '{name}' is not allowed."
            )
        return getattr(self._employee, name)

    # Ensure that formatting works as expected
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._ALLOWED_ATTRS)
        return f"<SafeEmployeeProxy {attrs}>"


def _filter_employees(dept_name: str) -> List[Employee]:
    """
    Return a list of employees belonging to the specified department.
    Case-insensitive comparison is used for robustness.
    """
    dept_name_lower = dept_name.strip().lower()
    return [
        emp for emp in EMPLOYEES
        if emp.department.strip().lower() == dept_name_lower
    ]


def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        Name of the department to filter employees by.
    template : str
        String containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        Concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If restricted fields are accessed or an unexpected error occurs.
    """
    if not isinstance(dept_name, str) or not isinstance(template, str):
        raise ValueError("Both dept_name and template must be strings.")

    try:
        employees = _filter_employees(dept_name)
        if not employees:
            return f"No employees found in department '{dept_name}'."

        formatted_entries = []

        # Pre-compile a regex to find placeholders like {employee.<attr>}
        placeholder_pattern = re.compile(r"\{(?P<obj>[^.]+)\.(?P<attr>[^\}]+)\}")

        for emp in employees:
            proxy = _SafeEmployeeProxy(emp)

            # Render the template safely
            def replace_placeholder(match: re.Match) -> str:
                obj_name = match.group("obj")
                attr_name = match.group("attr")

                if obj_name != "employee":
                    # Unsupported object name; treat as literal
                    return match.group(0)

                try:
                    value = getattr(proxy, attr_name)
                except AttributeError as exc:
                    raise ValueError(
                        f"Attribute '{attr_name}' not found for employee "
                        f"'{emp.name}'."
                    ) from exc

                return str(value)

            formatted = placeholder_pattern.sub(replace_placeholder, template)
            formatted_entries.append(formatted)

        return "\n".join(formatted_entries)

    except Exception as exc:
        # Wrap any exception into a ValueError with context
        raise ValueError(f"Failed to assemble employee list: {exc}") from exc


# ----------------------------------------------------------------------
# Example usage (commented out; remove comments to run)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    # Example template
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        output = assemble_employee_list("Engineering", tmpl)
        print(output)
    except ValueError as e:
        print(f"Error: {e}")