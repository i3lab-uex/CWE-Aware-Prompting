import re
from dataclasses import dataclass, field
from typing import List

# ----------------------------------------------------------------------
# Minimal Employee model used for demonstration purposes.
# In a real system this would be imported from the application's data layer.
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)          # Sensitive field – should not be exposed.
    personal_email: str = field(repr=False)   # Sensitive field – should not be exposed.

# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Produce a formatted employee directory for the given division.
    
    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string containing placeholders of the form '{employee.field}'.
    
    Returns
    -------
    str
        The roster string with placeholders replaced by actual employee data.
    
    Raises
    ------
    ValueError
        If a restricted field is requested in the template or an unexpected error occurs.
    """
    # ------------------------------------------------------------------
    # 1. Validate placeholders: disallow sensitive fields.
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r'\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}')
    allowed_fields = {"name", "position", "department"}  # Exclude salary and personal_email
    
    for match in placeholder_pattern.finditer(roster_template):
        field_name = match.group(1)
        if field_name not in allowed_fields:
            raise ValueError(f"Access to restricted field '{field_name}' is prohibited.")
    
    # ------------------------------------------------------------------
    # 2. Retrieve employees belonging to the specified division.
    #    In a real application this would query a database or data store.
    # ------------------------------------------------------------------
    try:
        all_employees: List[Employee] = _fetch_all_employees()
        division_employees = [emp for emp in all_employees if emp.department == division_name]
    except Exception as exc:
        raise ValueError(f"Failed to fetch employees: {exc}") from exc
    
    # ------------------------------------------------------------------
    # 3. Build the roster string.
    # ------------------------------------------------------------------
    try:
        lines = []
        for emp in division_employees:
            line = roster_template.format(employee=emp)
            lines.append(line)
        return "\n".join(lines)
    except Exception as exc:
        raise ValueError(f"Error rendering roster: {exc}") from exc

# ----------------------------------------------------------------------
# Mock function to simulate data retrieval.
# In production, replace this with actual database access logic.
def _fetch_all_employees() -> List[Employee]:
    return [
        Employee(name="Alice Smith", position="Engineer", department="Engineering",
                 salary=95000, personal_email="alice.smith@example.com"),
        Employee(name="Bob Johnson", position="Manager", department="Engineering",
                 salary=120000, personal_email="bob.johnson@example.com"),
        Employee(name="Carol Williams", position="Designer", department="Design",
                 salary=85000, personal_email="carol.williams@example.com"),
    ]

# ----------------------------------------------------------------------
# Example usage (for illustration only; remove or comment out in production)
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_team_roster("Engineering", template))