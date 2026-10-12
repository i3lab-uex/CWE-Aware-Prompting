import re
from dataclasses import dataclass, field
from typing import List

# ----------------------------------------------------------------------
# Employee model and sample data (replace with real source in production)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)           # sensitive
    personal_email: str = field(repr=False)     # sensitive

# Example dataset – in real usage this would come from a database or API
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Lee", "Analyst", "Finance", 70000, "carol@company.com"),
    # ... more employees ...
]

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted roster string with one employee per line.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary or personal_email)
        or contains unknown placeholders, or if any unexpected error occurs.
    """
    # Allowed and restricted fields
    allowed_fields = {"name", "position", "department"}
    restricted_fields = {"salary", "personal_email"}

    # Find all placeholders in the template
    placeholders = re.findall(r"\{employee\.([^\}]+)\}", roster_template)

    # Validate placeholders
    for field_name in placeholders:
        if field_name in restricted_fields:
            raise ValueError(f"Restricted field '{field_name}' used in template.")
        if field_name not in allowed_fields:
            raise ValueError(f"Unknown placeholder '{field_name}' used in template.")

    # Filter employees by division
    filtered_employees = [e for e in EMPLOYEES if e.department == division_name]

    # Build roster lines
    try:
        roster_lines = []
        for emp in filtered_employees:
            context = {
                "name": emp.name,
                "position": emp.position,
                "department": emp.department,
            }
            roster_lines.append(roster_template.format(**context))
        return "\n".join(roster_lines)
    except Exception as exc:
        # Wrap any formatting or other unexpected errors
        raise ValueError("An error occurred while generating the roster.") from exc

# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(generate_team_roster("Engineering", template))
    except ValueError as err:
        print(f"Error: {err}")