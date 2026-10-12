# -*- coding: utf-8 -*-
"""
Employee directory builder.

The module defines a single public function :func:`build_team_directory`
which produces a formatted string containing all employees that belong to
the supplied department.  The function guards against accidental exposure
of sensitive data such as ``salary`` or ``personal_email``.

The code is intentionally defensive: any attempt to reference a sensitive
attribute via the format template triggers a :class:`ValueError`.  This
prevents accidental leakage of confidential information (CWE‑200).
"""

from __future__ import annotations

import re
from typing import List


# --------------------------------------------------------------------------- #
# Minimal Employee data structure used by the function.
# In a real application this would be imported from another module.
class Employee:
    """
    Simple representation of an employee.

    Attributes
    ----------
    name : str
        Full name.
    position : str
        Job title.
    department : str
        Department to which the employee belongs.
    salary : float
        Annual salary (sensitive).
    personal_email : str
        Personal email address (sensitive).
    """

    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(
        self,
        name: str,
        position: str,
        department: str,
        salary: float,
        personal_email: str,
    ) -> None:
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# --------------------------------------------------------------------------- #
# Dummy data – in a real application this would come from a database or
# an external service.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Product", 105000.0, "bob.johnson@example.com"),
    Employee("Carol Williams", "Software Engineer", "Engineering", 97000.0, "carol.williams@example.com"),
    Employee("David Brown", "HR Specialist", "Human Resources", 65000.0, "david.brown@example.com"),
]


# --------------------------------------------------------------------------- #
def _validate_template(template: str) -> None:
    """
    Validate that the template does not reference sensitive attributes.

    Parameters
    ----------
    template : str
        The format string supplied by the caller.

    Raises
    ------
    ValueError
        If a sensitive attribute is referenced or the template is malformed.
    """
    # Allowed placeholders are of the form {employee.<field>}.
    # Reject any that reference 'salary' or 'personal_email'.
    sensitive_fields = {"salary", "personal_email"}
    # Find all placeholders
    placeholders = re.findall(r"\{([^}]+)\}", template)
    for ph in placeholders:
        # Ensure the placeholder is of the form employee.<field>
        if not ph.startswith("employee."):
            raise ValueError(f"Unsupported placeholder: {{{ph}}}")
        field = ph.split(".", 1)[1]
        if field in sensitive_fields:
            raise ValueError(f"Access to sensitive attribute '{field}' is prohibited.")


def _format_employee(employee: Employee, template: str) -> str:
    """
    Format a single employee using the provided template.

    Parameters
    ----------
    employee : Employee
        The employee instance to format.
    template : str
        Format string that has been validated.

    Returns
    -------
    str
        The formatted employee record.
    """
    # Build a simple namespace dictionary for formatting.
    ns = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
    }
    try:
        return template.format(**ns)
    except KeyError as exc:
        # This should not happen because we validated the template.
        raise ValueError(f"Missing field in employee data: {exc}") from exc
    except Exception as exc:
        # Catch all other formatting errors.
        raise ValueError(f"Formatting error: {exc}") from exc


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a directory listing for all employees in the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department whose employees should be listed.
    format_template : str
        A template string containing placeholders such as
        ``{employee.name}``, ``{employee.position}`` and
        ``{employee.department}``.  Sensitive fields are not allowed.

    Returns
    -------
    str
        A newline‑separated string containing the formatted employee entries.

    Raises
    ------
    ValueError
        If a sensitive attribute is referenced in the template,
        if formatting fails, or if no employees are found for the
        requested department.
    """
    # 1. Validate the template against sensitive data.
    _validate_template(format_template)

    # 2. Filter employees belonging to the requested department (case‑insensitive).
    matching = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    if not matching:
        raise ValueError(f"No employees found in department '{dept_name}'")

    # 3. Format each employee and join them.
    formatted_entries = [_format_employee(emp, format_template) for emp in matching]

    return "\n".join(formatted_entries)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", template))