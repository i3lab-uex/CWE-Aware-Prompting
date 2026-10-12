#!/usr/bin/env python3
"""
Secure employee roster compiler.

The module defines a function `compile_department_roster` that formats a
directory string for employees belonging to a given department.
It protects sensitive information such as `salary` and `personal_email`
by rejecting any template that tries to access those attributes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


# --------------------------------------------------------------------------- #
#  Employee model (minimal for demonstration purposes)
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # sensitive
    personal_email: str = field(repr=False)   # sensitive

# Example global list of employees – in a real system this would come from
# a database or an external data source.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000.0, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 75000.0, "carol@company.com"),
    # ... more employees ...
]


# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #
_SENSITIVE_FIELDS = {"salary", "personal_email"}
_PLACEHOLDER_RE = re.compile(r"\{([^}]+)\}")


def _check_template_safety(template: str) -> None:
    """
    Ensure that the template does not reference sensitive fields.

    Raises:
        ValueError: if a sensitive field is found in the template.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        expr = match.group(1).strip()
        # We only support simple `employee.<attr>` expressions.
        if "." not in expr:
            continue
        _, attr = expr.split(".", 1)
        if attr in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Template attempts to access sensitive field `{attr}`"
            )


def _format_employee(employee: Employee, template: str) -> str:
    """
    Safely format a single employee record using the provided template.

    Raises:
        ValueError: if formatting fails for any reason.
    """
    try:
        # Use a simple mapping with 'employee' key
        context = {"employee": employee}
        return template.format(**context)
    except Exception as exc:
        raise ValueError(f"Failed to format employee {employee.name!r}: {exc}") from exc


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted roster for all employees in the specified department.

    Args:
        division: The name of the department to filter by.
        template_str: A format string containing placeholders like
                      `{employee.name}` or `{employee.position}`.

    Returns:
        A string containing one formatted line per employee, separated by newlines.
        If no employees match the division, an empty string is returned.

    Raises:
        ValueError: If the template attempts to expose sensitive information
                    (e.g., salary or personal_email) or if any other error occurs.
    """
    # Validate the template early
    _check_template_safety(template_str)

    # Filter employees by department (case‑insensitive match)
    matching = [emp for emp in EMPLOYEES if emp.department.lower() == division.lower()]

    # Format each employee
    formatted_lines = []
    for emp in matching:
        formatted_lines.append(_format_employee(emp, template_str))

    return "\n".join(formatted_lines)


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(compile_department_roster("Engineering", template))