# -*- coding: utf-8 -*-
"""
Utility for generating a team directory from a template string.
"""

from __future__ import annotations

import re
from typing import List, Any


# ----------------------------------------------------------------------
# Assume an Employee class is defined elsewhere in the code base.
# For illustration purposes we provide a minimal stub here. In real usage
# this class would be imported from its module.
# ----------------------------------------------------------------------
class Employee:
    """
    Simple representation of an employee.

    Attributes
    ----------
    name : str
        Full name of the employee.
    position : str
        Job title / position.
    department : str
        Department name.
    salary : float
        Annual salary (sensitive).
    personal_email : str
        Personal email address (sensitive).
    """

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

    def __repr__(self) -> str:
        return (
            f"Employee(name={self.name!r}, position={self.position!r}, "
            f"department={self.department!r})"
        )


# ----------------------------------------------------------------------
# Global employee registry
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = []


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted directory for all employees belonging to ``team``.

    Parameters
    ----------
    team : str
        Department name used for filtering employees.
    template_text : str
        Text containing placeholders in the form ``{employee.<attribute>}``.

    Returns
    -------
    str
        The concatenated directory entries for the selected team.

    Raises
    ------
    ValueError
        If the template tries to expose sensitive information (salary or
        personal_email) or if any other error occurs during formatting.
    """
    # --------------------------------------------------------------
    # 1. Validate that the template does not request sensitive data
    # --------------------------------------------------------------
    sensitive_keys = {"salary", "personal_email"}
    # Find all placeholders that start with employee.
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    for match in placeholder_pattern.finditer(template_text):
        key = match.group(1)
        if key in sensitive_keys:
            raise ValueError(
                f"Attempt to expose sensitive attribute '{key}' in template."
            )

    # --------------------------------------------------------------
    # 2. Filter employees by department
    # --------------------------------------------------------------
    filtered_employees = [e for e in EMPLOYEES if e.department == team]

    # --------------------------------------------------------------
    # 3. Format each employee record
    # --------------------------------------------------------------
    formatted_entries: List[str] = []
    for emp in filtered_employees:
        try:
            # We pass a mapping that only contains non-sensitive attributes.
            # Any attempt to access an attribute not present will raise KeyError.
            entry = template_text.format(employee=emp)
        except Exception as exc:  # pragma: no cover
            raise ValueError(
                f"Failed to format entry for employee '{emp.name}'. "
                f"Original error: {exc}"
            ) from exc
        formatted_entries.append(entry)

    # --------------------------------------------------------------
    # 4. Return the final directory string
    # --------------------------------------------------------------
    return "\n".join(formatted_entries)


# ----------------------------------------------------------------------
# Example usage (commented out; remove or modify for real testing)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the global registry with sample data
    EMPLOYEES.extend(
        [
            Employee("Alice Smith", "Developer", "Engineering", 90000, "alice@example.com"),
            Employee("Bob Jones", "Manager", "Engineering", 120000, "bob@example.com"),
            Employee("Carol Lee", "Analyst", "Marketing", 70000, "carol@example.com"),
        ]
    )

    tmpl = (
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
    )
    try:
        directory = build_team_directory("Engineering", tmpl)
        print(directory)
    except ValueError as e:
        print(f"Error: {e}")