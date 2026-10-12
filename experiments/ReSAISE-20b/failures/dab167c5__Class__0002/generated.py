import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# For demonstration purposes we define a minimal stub here.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global employee list (in a real application this would come from a database)
EMPLOYEES: List[Employee] = []

def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        The department name to filter employees by.
    template_str : str
        Template string containing placeholders in the form `{employee.field}`.

    Returns
    -------
    str
        A multi-line string with each employee's information formatted according to
        `template_str`.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive fields (`salary` or `personal_email`)
        or if any other error occurs during processing.
    """
    # Regular expression to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    # Validate that no sensitive data is requested
    for match in placeholder_pattern.finditer(template_str):
        key = match.group(1).strip()
        # Accept only keys that start with 'employee.' and are followed by a single field
        if not key.startswith("employee."):
            raise ValueError(f"Unsupported placeholder '{match.group(0)}'")
        field_name = key.split(".", 1)[1]
        if field_name in {"salary", "personal_email"}:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

    # Filter employees by department
    filtered_employees = [e for e in EMPLOYEES if e.department == team]

    # Build the output string
    lines = []
    try:
        for employee in filtered_employees:
            formatted_line = template_str
            # Replace each placeholder with the actual attribute value
            for match in placeholder_pattern.finditer(template_str):
                key = match.group(1).strip()
                field_name = key.split(".", 1)[1]
                # Use getattr to fetch the attribute; raise if missing
                value = getattr(employee, field_name)
                formatted_line = formatted_line.replace(match.group(0), str(value))
            lines.append(formatted_line)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to meet the spec
        raise ValueError(f"Failed to generate roster: {exc}") from exc

    return "\n".join(lines)