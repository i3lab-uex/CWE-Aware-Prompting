#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple employee directory generator that safely renders a template for
employees belonging to a specified department.

The implementation deliberately avoids exposing sensitive attributes such as
`salary` and `personal_email`. If the template tries to access these fields,
or if any other exception occurs during rendering, a ValueError is raised.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field, fields
from typing import List, Any

# --------------------------------------------------------------------------- #
# Employee model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """Represents an employee in the organization."""
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# --------------------------------------------------------------------------- #
# Sample data (in a real system this would come from a database or other source)
# --------------------------------------------------------------------------- #

EMPLOYEES: List[Employee] = [
    Employee(name="Alice Smith", position="Software Engineer",
             department="Engineering", salary=95000.0,
             personal_email="alice.smith@example.com"),
    Employee(name="Bob Johnson", position="Product Manager",
             department="Product", salary=115000.0,
             personal_email="bob.johnson@example.com"),
    Employee(name="Carol White", position="Designer",
             department="Design", salary=75000.0,
             personal_email="carol.white@example.com"),
    Employee(name="David Brown", position="DevOps Engineer",
             department="Engineering", salary=88000.0,
             personal_email="david.brown@example.com"),
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts all field names from a format string.

    Uses a regular expression that matches `{field}` patterns.
    """
    return set(re.findall(r"{([a-zA-Z_][a-zA-Z0-9_]*)}", template))

def _validate_no_sensitive_fields(placeholders: set[str]) -> None:
    """
    Raises ValueError if any placeholder refers to a sensitive field.
    """
    sensitive = {"salary", "personal_email"}
    if placeholders & sensitive:
        raise ValueError(f"Template contains disallowed fields: {placeholders & sensitive}")

def _employee_to_dict(emp: Employee) -> dict[str, Any]:
    """
    Converts an Employee instance to a dictionary suitable for string formatting.
    Only non-sensitive fields are included.
    """
    allowed_fields = {"name", "position", "department"}
    return {k: getattr(emp, k) for k in allowed_fields}

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def build_team_directory(team: str, template_text: str) -> str:
    """
    Generates a formatted directory string for all employees in the specified
    department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_text : str
        A format string containing placeholders such as `{employee.name}`.

    Returns
    -------
    str
        A single string containing one rendered line per employee in the team.

    Raises
    ------
    ValueError
        If the template references sensitive fields or any error occurs during
        rendering.
    """
    try:
        # 1. Parse placeholders from the template
        placeholders = _extract_placeholders(template_text)

        # 2. Validate that no sensitive fields are referenced
        _validate_no_sensitive_fields(placeholders)

        # 3. Filter employees by department
        team_employees = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
        if not team_employees:
            return ""  # No employees found for the requested department

        # 4. Render each employee's line
        rendered_lines = []
        for emp in team_employees:
            context = _employee_to_dict(emp)
            # Prefix placeholders with 'employee.' as expected in template
            # e.g., {employee.name} -> context['name']
            rendered = template_text.format(**{"employee." + k: v for k, v in context.items()})
            rendered_lines.append(rendered)

        # 5. Join all lines into a single string
        return "\n".join(rendered_lines)

    except Exception as exc:
        # Wrap any exception into a ValueError with a clear message
        raise ValueError(f"Failed to build directory: {exc}") from exc

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        output = build_team_directory("Engineering", tmpl)
        print(output)
    except ValueError as e:
        sys.stderr.write(str(e) + "\n")