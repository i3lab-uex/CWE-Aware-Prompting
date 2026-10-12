#!/usr/bin/env python3
"""
Employee directory builder.

The module defines a simple Employee class and a global registry of employees.
`build_team_directory` produces a formatted directory for the requested
department using a user‑supplied template string.  The function guards against
access to sensitive fields (`salary`, `personal_email`) and raises a
`ValueError` when such access is attempted or if any other error occurs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


# --------------------------------------------------------------------------- #
# Employee model and registry
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """Simple employee record."""
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # sensitive
    personal_email: str = field(repr=False)   # sensitive


# A global registry that would normally be populated from a database or
# external source.  For the purposes of this module we keep it in memory.
EMPLOYEES: List[Employee] = [
    Employee(
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        salary=95000.0,
        personal_email="alice.smith@example.com",
    ),
    Employee(
        name="Bob Johnson",
        position="DevOps Engineer",
        department="Engineering",
        salary=88000.0,
        personal_email="bob.johnson@example.com",
    ),
    Employee(
        name="Carol Williams",
        position="HR Manager",
        department="Human Resources",
        salary=72000.0,
        personal_email="carol.williams@example.com",
    ),
]


# --------------------------------------------------------------------------- #
# Directory builder
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Fields that are considered sensitive and must not be exposed
SENSITIVE_FIELDS = {"salary", "personal_email"}


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory for all employees in ``dept_name``.

    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    format_template : str
        A template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The directory as a single string with each employee on its own line.

    Raises
    ------
    ValueError
        If the template references a sensitive field or if any other error occurs.
    """
    # 1. Validate the template for disallowed fields
    try:
        placeholders = PLACEHOLDER_PATTERN.findall(format_template)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Invalid template regex: {exc}") from exc

    for field_name in placeholders:
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

    # 2. Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not dept_employees:
        return f"No employees found in department '{dept_name}'."

    # 3. Render each employee using the template
    lines = []
    for emp in dept_employees:
        try:
            # Build a safe mapping for placeholder replacement
            context = {
                "employee.name": emp.name,
                "employee.position": emp.position,
                "employee.department": emp.department,
            }
            # Replace placeholders
            line = PLACEHOLDER_PATTERN.sub(
                lambda m: context.get(m.group(0), ""), format_template
            )
            lines.append(line)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Error rendering employee {emp.name}: {exc}") from exc

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(build_team_directory("Engineering", template))
    except ValueError as err:
        print(f"Error: {err}")