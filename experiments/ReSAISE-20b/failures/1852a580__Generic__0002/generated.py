import re
from typing import List

# ----------------------------------------------------------------------
# Example Employee class (replace with the real implementation)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary          # Restricted
        self.personal_email = personal_email  # Restricted

# ----------------------------------------------------------------------
# Helper: Return all employees (replace with real data source)
# ----------------------------------------------------------------------
def get_all_employees() -> List[Employee]:
    """Stub: Replace with real data retrieval logic."""
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@corp.com"),
        Employee("Bob Jones",   "Manager",  "Engineering", 120000, "bob@corp.com"),
        Employee("Carol Lee",   "Analyst",  "Finance",    75000, "carol@corp.com"),
    ]

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        Department name to filter employees.
    roster_template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted employee directory, one employee per line.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary or personal_email)
        or if an unexpected error occurs during formatting.
    """
    # Detect restricted field usage
    restricted_patterns = [r'\{employee\.salary\}', r'\{employee\.personal_email\}']
    for pat in restricted_patterns:
        if re.search(pat, roster_template):
            raise ValueError(f"Template contains restricted field: {pat}")

    employees = get_all_employees()
    filtered = [e for e in employees if e.department.lower() == division_name.lower()]
    if not filtered:
        return f"No employees found in department '{division_name}'."

    lines = []
    for emp in filtered:
        try:
            # Build a simple mapping for the placeholders
            context = {
                'employee.name': emp.name,
                'employee.position': emp.position,
                # Additional safe fields can be added here if needed
            }
            formatted = roster_template.format(**context)
            lines.append(formatted)
        except Exception as exc:
            raise ValueError(f"Failed to format employee '{emp.name}': {exc}") from exc

    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_team_roster("Engineering", template))