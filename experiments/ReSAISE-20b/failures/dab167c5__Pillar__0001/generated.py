from __future__ import annotations

import re
from typing import Iterable, List

# Assuming an Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float
# personal_email: str

class Employee:
    """Placeholder for the actual Employee class."""
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not request sensitive data.
    Raises ValueError if a forbidden placeholder is found.
    """
    forbidden = {"salary", "personal_email"}
    # Find all placeholders of the form {employee.<field>}
    placeholders = re.findall(r"\{employee\.([^\}]+)\}", template)
    for field in placeholders:
        if field in forbidden:
            raise ValueError(
                f"Template contains a forbidden placeholder: {{employee.{field}}}"
            )


def create_team_roster(team: str, template_str: str,
                       employees: Iterable[Employee]) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_str : str
        A format string containing placeholders like `{employee.name}`.
    employees : Iterable[Employee]
        Collection of Employee objects to search.

    Returns
    -------
    str
        The concatenated formatted string for all employees in the department.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data or if formatting fails.
    """
    # Validate the template once
    _validate_template(template_str)

    # Filter employees by department
    team_members: List[Employee] = [
        emp for emp in employees if emp.department == team
    ]

    # If no members, return an empty string
    if not team_members:
        return ""

    formatted_lines: List[str] = []
    for emp in team_members:
        try:
            line = template_str.format(employee=emp)
        except Exception as exc:  # pragma: no cover
            raise ValueError(
                f"Failed to format employee '{emp.name}': {exc}"
            ) from exc
        formatted_lines.append(line)

    return "\n".join(formatted_lines)