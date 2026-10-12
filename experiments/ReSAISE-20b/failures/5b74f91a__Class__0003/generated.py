import re
from typing import List

# Assuming an Employee class exists in the context. 
# For illustration, a minimal stub is provided below; replace or remove it when integrating.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = 0.0, personal_email: str = ""):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of all employees (populate this with real data in your application)
EMPLOYEES: List[Employee] = []


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Args:
        dept_name: Department name to filter employees.
        format_template: A string containing placeholders like
                         '{employee.name}', '{employee.position}'.

    Returns:
        A newline‑separated string with each employee formatted
        according to `format_template`.

    Raises:
        ValueError: If the template attempts to access sensitive data
                    (salary or personal_email) or if formatting fails.
    """
    # Define the set of fields that are considered sensitive
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = set(placeholder_pattern.findall(format_template))

    # Check for disallowed (sensitive) fields
    if SENSITIVE_FIELDS & placeholders:
        raise ValueError(
            f"Template contains sensitive fields: {SENSITIVE_FIELDS & placeholders}"
        )

    # Prepare the directory lines
    directory_lines = []

    for emp in EMPLOYEES:
        if emp.department.lower() != dept_name.lower():
            continue

        # Build a mapping of allowed attributes
        attr_map = {}
        for field in placeholders:
            try:
                value = getattr(emp, field)
            except AttributeError as exc:
                raise ValueError(
                    f"Employee has no attribute '{field}'."
                ) from exc
            attr_map[field] = value

        # Format the line using format_map to avoid KeyError
        try:
            formatted_line = format_template.format(**attr_map)
        except Exception as exc:
            raise ValueError(
                f"Error formatting employee '{emp.name}': {exc}"
            ) from exc

        directory_lines.append(formatted_line)

    return "\n".join(directory_lines)