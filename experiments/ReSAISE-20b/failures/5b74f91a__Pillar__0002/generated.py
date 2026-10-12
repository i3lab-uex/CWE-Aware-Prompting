#!/usr/bin/env python3
"""
Employee directory builder.

This module contains a single public function :func:`build_team_directory`
which formats a list of employees belonging to a given department according
to a supplied template.  The function protects against accidental exposure of
sensitive fields such as ``salary`` and ``personal_email``.

The module deliberately keeps the employee data in a global list to avoid
the need for external database connections.  In a real‑world application,
this data would be fetched from a secure source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import List


# --------------------------------------------------------------------------- #
#  Employee model and sample data
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Sensitive
    personal_email: str    # Sensitive


# Sample data – in practice this would come from a secure database
EMPLOYEES: List[Employee] = [
    Employee(
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        salary=120000.0,
        personal_email="alice.smith@example.com",
    ),
    Employee(
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        salary=110000.0,
        personal_email="bob.johnson@example.com",
    ),
    Employee(
        name="Carol Williams",
        position="Data Analyst",
        department="Engineering",
        salary=95000.0,
        personal_email="carol.williams@example.com",
    ),
]


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a directory of employees for *dept_name* using *format_template*.

    Parameters
    ----------
    dept_name : str
        The department whose employees should be included.
    format_template : str
        A template string containing placeholders in the form ``{employee.field}``.
        Allowed fields are those defined on :class:`Employee` **except** for
        ``salary`` and ``personal_email``.

    Returns
    -------
    str
        A string containing the formatted information for each employee in the
        specified department, one entry per line.

    Raises
    ------
    ValueError
        If the template attempts to access a sensitive field or if any other
        error occurs during formatting.
    """
    # ----------------------------------------------------------------------- #
    # 1. Validate template for sensitive fields
    # ----------------------------------------------------------------------- #

    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(format_template)

    # Fields that are considered sensitive
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    for field_name in placeholders:
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(
                f"Template contains sensitive field '{field_name}'. "
                "Access is prohibited."
            )

    # ----------------------------------------------------------------------- #
    # 2. Filter employees by department
    # ----------------------------------------------------------------------- #

    filtered_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    if not filtered_employees:
        return f"No employees found in department '{dept_name}'."

    # ----------------------------------------------------------------------- #
    # 3. Format each employee
    # ----------------------------------------------------------------------- #

    formatted_lines: List[str] = []

    for emp in filtered_employees:
        try:
            # Replace placeholders with actual values
            line = placeholder_pattern.sub(
                lambda m: str(getattr(emp, m.group(1))), format_template
            )
        except AttributeError as exc:
            # This should not happen because we already validated fields,
            # but guard against unforeseen attribute errors.
            raise ValueError(
                f"Failed to format employee '{emp.name}': {exc}"
            ) from exc
        except Exception as exc:
            # Catch any other unexpected error during formatting.
            raise ValueError(
                f"Unexpected error while formatting employee '{emp.name}': {exc}"
            ) from exc

        formatted_lines.append(line)

    # ----------------------------------------------------------------------- #
    # 4. Return joined string
    # ----------------------------------------------------------------------- #

    return "\n".join(formatted_lines)


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(build_team_directory("Engineering", template))