import re
from typing import List

# Assume Employee is defined elsewhere in the codebase with attributes:
# name, position, department, salary, personal_email
# For type checking purposes we can declare a minimal protocol.
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str


# In a real application this list would come from a database or other data source.
EMPLOYEES: List[Employee] = []  # populated elsewhere


def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The name of the department to filter employees by.
    list_template : str
        A string template containing placeholders like '{employee.name}' or
        '{employee.position}'.  The placeholders are replaced with actual data.

    Returns
    -------
    str
        A string containing the formatted directory for all employees in the
        specified department.

    Raises
    ------
    ValueError
        If the template contains a restricted field such as 'salary' or
        'personal_email', or if an unexpected error occurs during formatting.
    """
    # Fields that are considered sensitive and must not be exposed
    RESTRICTED_FIELDS = {"salary", "personal_email"}

    # Find all placeholders in the template.
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = set(placeholder_pattern.findall(list_template))

    # Ensure no restricted fields are requested.
    for field in placeholders:
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")

    # Filter employees by department.
    filtered_employees = [e for e in EMPLOYEES if e.department == team_name]

    # Build the result string.
    lines = []
    for employee in filtered_employees:
        try:
            # Perform the replacement safely.
            line = list_template.format(employee=employee)
            lines.append(line)
        except Exception as exc:
            # Wrap any unexpected exception in a ValueError.
            raise ValueError(f"Failed to format employee '{employee.name}': {exc}") from exc

    return "\n".join(lines)