import re
from typing import List

# Assume Employee is defined elsewhere in the project.
# For type checking we provide a minimal stub that can be replaced with the real class.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = None, personal_email: str = None):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# In a real application this would be replaced with the actual data source.
EMPLOYEES: List[Employee] = []

# Regex to find placeholders in the template
PLACEHOLDER_RE = re.compile(r'\{([^{}]+)\}')

# Set of fields that are considered sensitive
SENSITIVE_FIELDS = {'salary', 'personal_email'}


def create_team_roster(team: str, template_str: str) -> str:
    """
    Build a formatted directory for all employees belonging to ``team``.

    Parameters
    ----------
    team : str
        Department name.
    template_str : str
        String containing placeholders like ``{employee.name}``.

    Returns
    -------
    str
        A newline separated string with each employee formatted according to
        ``template_str``.

    Raises
    ------
    ValueError
        If the template references a sensitive field or if formatting fails.
    """
    # Detect any attempt to access sensitive data
    for match in PLACEHOLDER_RE.finditer(template_str):
        placeholder = match.group(1).strip()
        # Expect placeholders in the form 'employee.field'
        parts = placeholder.split('.')
        if len(parts) != 2 or parts[0] != 'employee':
            raise ValueError(f"Unsupported placeholder '{placeholder}'. "
                             "Only 'employee.<field>' is allowed.")
        field_name = parts[1]
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited.")

    # Filter employees by department
    team_members = [e for e in EMPLOYEES if e.department == team]

    formatted_lines: List[str] = []
    for emp in team_members:
        try:
            line = template_str.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        formatted_lines.append(line)

    return '\n'.join(formatted_lines)