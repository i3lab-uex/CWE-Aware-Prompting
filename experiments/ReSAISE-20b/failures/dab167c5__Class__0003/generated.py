import re
from typing import List

# Assume Employee is defined elsewhere with attributes:
# name, position, department, salary, personal_email
# For demonstration purposes we define a minimal stub here.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = None, personal_email: str = None):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


def create_team_roster(team: str, template_str: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        The name of the department whose employees are to be listed.
    template_str : str
        A format string that may contain placeholders such as
        '{employee.name}', '{employee.position}' etc.

    Returns
    -------
    str
        A newline separated string containing the formatted information for each
        employee in the requested department.

    Raises
    ------
    ValueError
        If the template references a sensitive attribute (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Allowed (non‑sensitive) fields that can appear in the template
    allowed_fields = {"name", "position", "department"}

    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(template_str)

    # Reject any use of sensitive fields
    for field in placeholders:
        if field not in allowed_fields:
            raise ValueError(
                f"Access to sensitive attribute '{field}' is not permitted."
            )

    # In a real system we would query the database or data store here.
    # For this implementation we assume there is a global list `ALL_EMPLOYEES`.
    # Replace the following line with your actual data source.
    all_employees: List[Employee] = getattr(
        globals(), "ALL_EMPLOYEES", []
    )

    # Filter employees belonging to the requested department
    dept_employees = [
        e for e in all_employees if getattr(e, "department", None) == team
    ]

    # Build the directory string
    lines = []
    for emp in dept_employees:
        try:
            line = template_str.format(employee=emp)
        except Exception as exc:
            raise ValueError(
                f"Failed to format employee data for '{emp.name}': {exc}"
            ) from exc
        lines.append(line)

    return "\n".join(lines)