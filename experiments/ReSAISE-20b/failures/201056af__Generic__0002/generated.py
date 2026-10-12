import re
from dataclasses import dataclass, fields
from typing import List

# --------------------------------------------------------------------
# Sample Employee definition (for demonstration only)
# In a real application this would be imported from your data module.
# --------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float  # restricted
    personal_email: str  # restricted

# Global list of all employees (this would normally come from a DB or other source)
ALL_EMPLOYEES: List[Employee] = []

# --------------------------------------------------------------------
# Build worker list implementation
# --------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        Department name to filter employees by.
    list_template : str
        Template string containing placeholders in the form `{employee.field}`.

    Returns
    -------
    str
        Formatted string representing the employee directory for the department.

    Raises
    ------
    ValueError
        If the template contains restricted fields (salary, personal_email) or an
        unexpected error occurs during processing.
    """
    # Fields that are considered sensitive and must not be exposed
    RESTRICTED_FIELDS = {"salary", "personal_email"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(list_template)

    # Check for restricted fields
    for field in placeholders:
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")

    # Filter employees by department
    dept_employees = [e for e in ALL_EMPLOYEES if e.department == team_name]

    # If no employees found, return an informative message
    if not dept_employees:
        return f"No employees found in department '{team_name}'."

    # Build the output string
    lines = []
    try:
        for emp in dept_employees:
            # Create a copy of the template and replace placeholders
            line = list_template
            for field in placeholders:
                value = getattr(emp, field)
                # Escape braces in the value to avoid formatting issues
                safe_value = str(value).replace("{", "{{").replace("}", "}}")
                line = line.replace(f"{{employee.{field}}}", safe_value)
            lines.append(line)
    except Exception as exc:
        # Any unexpected error is wrapped in a ValueError
        raise ValueError(f"An error occurred while building the worker list: {exc}") from exc

    return "\n".join(lines)