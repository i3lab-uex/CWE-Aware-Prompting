#!/usr/bin/env python3
"""
Employee directory generation module.

This module defines an `Employee` data class and a function
`create_team_roster(team: str, template_str: str) -> str`
that produces a formatted directory for employees belonging to
the specified department.  Accessing sensitive fields such as
`surname` or `personal_email` in the template is prohibited and
will raise a ValueError.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

# --------------------------------------------------------------------------- #
# Employee data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """Immutable representation of an employee."""
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # Sensitive data – hidden in repr
    personal_email: str = field(repr=False)   # Sensitive data – hidden in repr

# --------------------------------------------------------------------------- #
# Sample dataset (would normally come from a database or external service)
# --------------------------------------------------------------------------- #

EMPLOYEES: List[Employee] = [
    Employee(
        name="Alice Johnson",
        position="Software Engineer",
        department="Engineering",
        salary=95000.0,
        personal_email="alice.johnson@example.com"
    ),
    Employee(
        name="Bob Smith",
        position="Product Manager",
        department="Product",
        salary=105000.0,
        personal_email="bob.smith@example.com"
    ),
    Employee(
        name="Charlie Lee",
        position="Data Analyst",
        department="Engineering",
        salary=88000.0,
        personal_email="charlie.lee@example.com"
    ),
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _sanitize_template(template: str) -> None:
    """
    Ensure that the template does not reference sensitive fields.
    Raises ValueError if a forbidden field is detected.
    """
    # Define the set of disallowed keys
    forbidden_keys = {"salary", "personal_email"}

    # Find all identifiers inside {} braces
    placeholders = re.findall(r"\{([^{}]+)\}", template)
    for placeholder in placeholders:
        # Support nested attributes like employee.name
        key = placeholder.split(".")[-1]
        if key in forbidden_keys:
            raise ValueError(
                f"Access to sensitive field '{key}' is prohibited in the template."
            )

def _employee_to_dict(emp: Employee) -> dict:
    """
    Convert an Employee instance to a dictionary suitable for str.format_map.
    Excludes sensitive fields.
    """
    # Use the dataclass's __dict__ but filter out sensitive keys
    data = {
        k: v for k, v in emp.__dict__.items()
        if k not in {"salary", "personal_email"}
    }
    return data

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted directory listing for all employees in the
    specified department.

    Parameters:
        team (str): The department name to filter employees by.
        template_str (str): A format string containing placeholders
                            such as '{name}', '{position}'.

    Returns:
        str: A newline‑separated string with each employee formatted
             according to `template_str`.

    Raises:
        ValueError: If the template attempts to access sensitive data
                    or if any formatting error occurs.
    """
    # Validate the template for forbidden fields
    _sanitize_template(template_str)

    # Filter employees by department (case‑insensitive match)
    matching = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
    if not matching:
        return f"No employees found in department '{team}'."

    # Build the directory
    lines = []
    for emp in matching:
        try:
            formatted_line = template_str.format_map(_employee_to_dict(emp))
        except Exception as exc:  # Catch all formatting-related errors
            raise ValueError(
                f"Error formatting employee '{emp.name}': {exc}"
            ) from exc
        lines.append(formatted_line)

    return "\n".join(lines)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Name: {name}, Position: {position}"
    try:
        print(create_team_roster("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")