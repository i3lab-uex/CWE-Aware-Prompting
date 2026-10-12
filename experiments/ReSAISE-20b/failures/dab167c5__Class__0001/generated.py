import re
from typing import List

# --------------------------------------------------------------------
# Assume the following Employee class exists in the environment.
# --------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------
# Global list of all employees (for demonstration purposes).
# In a real system this would come from a database or other data source.
# --------------------------------------------------------------------
ALL_EMPLOYEES: List[Employee] = []

# --------------------------------------------------------------------
# Function to create a team roster
# --------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified team.

    Parameters
    ----------
    team : str
        The department name to filter employees.
    template_str : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted directory string.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive fields (salary,
        personal_email) or if any other error occurs during processing.
    """
    # 1. Validate that no sensitive data is requested
    forbidden_fields = {"salary", "personal_email"}
    # Find all placeholders in the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    for match in placeholder_pattern.finditer(template_str):
        field = match.group(1).strip()
        if field in forbidden_fields:
            raise ValueError(f"Access to sensitive field '{field}' is prohibited.")

    # 2. Filter employees by department
    try:
        team_members = [emp for emp in ALL_EMPLOYEES if emp.department == team]
    except Exception as exc:
        raise ValueError(f"Failed to filter employees: {exc}") from exc

    # 3. Build the directory string
    lines = []
    for emp in team_members:
        try:
            line = template_str.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Template formatting error for employee '{emp.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the global list with sample data
    ALL_EMPLOYEES.extend([
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@example.com"),
        Employee("Bob Jones", "Manager", "Engineering", 120000, "bob@example.com"),
        Employee("Carol White", "Analyst", "Finance", 70000, "carol@example.com"),
    ])

    template = "{employee.name} - {employee.position}"
    try:
        roster = create_team_roster("Engineering", template)
        print(roster)
    except ValueError as e:
        print(f"Error: {e}")