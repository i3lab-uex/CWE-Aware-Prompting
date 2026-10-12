import re
from typing import List

# Assume Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float   # Sensitive
# personal_email: str  # Sensitive

ALLOWED_FIELDS = {"name", "position", "department"}

def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a directory listing for all employees in the specified department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_str : str
        A format string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted directory string.

    Raises
    ------
    ValueError
        If a placeholder references sensitive data or any error occurs during formatting.
    """
    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(template_str)

    # Verify that all referenced fields are allowed
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unsupported field '{field}' is not permitted.")

    # Fetch employees belonging to the requested department
    try:
        from employee_module import Employee  # Import where Employee is defined
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to import Employee class.") from exc

    # Assume we have a global list `EMPLOYEES` or a function to retrieve them
    try:
        from employee_module import EMPLOYEES  # pragma: no cover
    except Exception as exc:
        raise ValueError("Failed to access employee data.") from exc

    # Filter employees by department
    dept_employees: List[Employee] = [e for e in EMPLOYEES if e.department == team]

    # Build the directory string
    lines = []
    for emp in dept_employees:
        try:
            # Create a mapping for allowed fields
            context = {f"employee.{field}": getattr(emp, field) for field in ALLOWED_FIELDS}
            # Replace placeholders safely
            line = template_str.format(**context)
            lines.append(line)
        except Exception as exc:
            raise ValueError(f"Failed to format employee record: {exc}") from exc

    return "\n".join(lines)