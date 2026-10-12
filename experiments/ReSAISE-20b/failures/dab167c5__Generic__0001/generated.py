from dataclasses import dataclass, fields
from typing import List

# --------------------------------------------------------------------------- #
# Employee model and a sample in‑memory data store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Sensitive
    personal_email: str   # Sensitive

# Sample data – in a real system this would come from a database or API
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 110000, "bob.johnson@example.com"),
    Employee("Carol Williams", "HR Specialist", "Human Resources", 70000, "carol.williams@example.com"),
    # ... more employees ...
]

# --------------------------------------------------------------------------- #
# Utility to safely format employee data
# --------------------------------------------------------------------------- #

def _safe_format(template: str, employee: Employee) -> str:
    """
    Format `template` with attributes from `employee`.  Raises ValueError
    if the template attempts to access sensitive fields.
    """
    # Define which attributes are considered safe
    SAFE_FIELDS = {f.name for f in fields(Employee) if f.name not in {"salary", "personal_email"}}

    # Find all placeholders in the template
    import re

    pattern = r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    placeholders = set(re.findall(pattern, template))

    # Check for disallowed accesses
    if not placeholders.issubset(SAFE_FIELDS):
        disallowed = placeholders - SAFE_FIELDS
        raise ValueError(f"Attempt to access sensitive fields: {', '.join(disallowed)}")

    # Build a dictionary for formatting
    data = {name: getattr(employee, name) for name in placeholders}
    return template.format(**data)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted directory for all employees in `team`.

    Parameters
    ----------
    team : str
        The department name to filter employees.
    template_str : str
        A format string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        A newline‑separated string with each employee formatted per the template.

    Raises
    ------
    ValueError
        If sensitive fields are referenced in `template_str` or if formatting fails.
    """
    # Validate arguments
    if not isinstance(team, str) or not isinstance(template_str, str):
        raise ValueError("Both 'team' and 'template_str' must be strings.")

    # Filter employees by department (case‑insensitive)
    filtered = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
    if not filtered:
        return f"No employees found in department '{team}'."

    # Format each employee safely
    formatted_lines = []
    for emp in filtered:
        try:
            line = _safe_format(template_str, emp)
            formatted_lines.append(line)
        except Exception as exc:
            raise ValueError(f"Formatting error for employee '{emp.name}': {exc}") from exc

    return "\n".join(formatted_lines)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_team_roster("Engineering", tmpl))