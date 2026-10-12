import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
class Employee:  # Dummy placeholder for type checking; real implementation is expected to exist.
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# In a real application, replace this with the actual data source
def _get_all_employees() -> List[Employee]:
    """Return a list of all employees. Replace with real data source."""
    return []

def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        The department name to filter employees.
    template_text : str
        A template string containing placeholders such as `{employee.name}` or
        `{employee.position}`.

    Returns
    -------
    str
        The formatted directory string with one entry per employee in the
        specified department.

    Raises
    ------
    ValueError
        If a placeholder attempts to access sensitive data (`salary` or
        `personal_email`) or if any other error occurs during formatting.
    """
    # 1. Detect sensitive placeholders
    SENSITIVE_KEYS = {"salary", "personal_email"}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    for match in placeholder_pattern.finditer(template_text):
        key = match.group(1).strip()
        if key in SENSITIVE_KEYS:
            raise ValueError(f"Access to sensitive field '{key}' is not allowed.")

    # 2. Retrieve employees and filter by department
    all_employees = _get_all_employees()
    filtered_emps = [emp for emp in all_employees if emp.department == team]

    # 3. Prepare the output
    lines = []
    for emp in filtered_emps:
        # Build a simple namespace dict for formatting
        ns = {
            "employee.name": emp.name,
            "employee.position": emp.position,
            # Expose only non-sensitive fields
        }
        try:
            line = template_text.format(**ns)
        except Exception as exc:
            raise ValueError(f"Failed to format template: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)