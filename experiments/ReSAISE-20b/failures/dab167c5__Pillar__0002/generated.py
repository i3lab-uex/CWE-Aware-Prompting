import re
from typing import List

# ------------------------------------------------------------------
# Minimal Employee model (in a real system this would be imported)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# Sample data store – in practice this would be replaced by a real
# database/query layer.  The function only reads from it; no
# modification of the collection is performed.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@corp.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 120000, "bob@corp.com"),
    Employee("Carol Lee", "HR Manager", "Human Resources", 80000, "carol@corp.com"),
]

# ------------------------------------------------------------------
# Helper: safe mapping that disallows sensitive fields
# ------------------------------------------------------------------
def _employee_mapping(emp: Employee) -> dict:
    """
    Return a dictionary of attributes that are safe to expose.
    Raises ValueError if an attempt is made to expose a sensitive
    attribute (salary or personal_email).
    """
    safe_attrs = {
        "name": emp.name,
        "position": emp.position,
        "department": emp.department
    }
    # The mapping key is always 'employee' to match the placeholder syntax.
    return {"employee": safe_attrs}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified team.

    Parameters
    ----------
    team : str
        The department name to filter employees.
    template_str : str
        A format string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        A newline‑separated string containing the formatted information for
        all employees in the specified department.

    Raises
    ------
    ValueError
        If a placeholder refers to a sensitive attribute (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Validate that the template does not request sensitive data
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(template_str):
        parts = match.group(1).split(".")
        if len(parts) != 2 or parts[0] != "employee":
            raise ValueError(f"Unsupported placeholder format: {{{match.group(1)}}}")
        attr = parts[1]
        if attr in ("salary", "personal_email"):
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited")

    # Build the directory
    lines = []
    for emp in EMPLOYEES:
        if emp.department != team:
            continue
        try:
            mapping = _employee_mapping(emp)
            # Use format_map to avoid KeyError for missing placeholders
            line = template_str.format_map(mapping)
        except Exception as exc:
            # Wrap any formatting error into ValueError
            raise ValueError(f"Formatting failed for employee {emp.name}: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)