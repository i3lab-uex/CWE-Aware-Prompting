import re
from dataclasses import dataclass
from typing import List

# -------------------------------------------------------------
# Example Employee class (in a real project this would be imported)
# -------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# -------------------------------------------------------------
# Dummy data – in a real scenario this would come from a DB or
# another module.  The function below operates on this list.
# -------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Johnson", "Engineer", "Engineering", 95000, "alice.johnson@example.com"),
    Employee("Bob Smith",     "Manager",   "Engineering", 120000, "bob.smith@example.com"),
    Employee("Carol White",   "Analyst",   "Finance",     85000, "carol.white@example.com"),
    # ... more employees ...
]

# -------------------------------------------------------------
# Function to create a team roster
# -------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted directory for all employees in the given department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_str : str
        A string containing placeholders in the form `{employee.field}`.

    Returns
    -------
    str
        The concatenated, formatted directory entries for the specified team.

    Raises
    ------
    ValueError
        If a placeholder refers to a sensitive field (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Fields that are considered sensitive
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    # Filter employees by department (case‑insensitive)
    team_members = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
    if not team_members:
        return ""  # No members found – return empty string

    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def replace_placeholder(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is not allowed.")
        # Ensure the employee has this attribute
        if not hasattr(employee, field_name):
            raise ValueError(f"Employee has no attribute '{field_name}'.")
        return str(getattr(employee, field_name))

    formatted_entries = []
    for employee in team_members:
        try:
            entry = placeholder_pattern.sub(replace_placeholder, template_str)
            formatted_entries.append(entry)
        except Exception as exc:
            # Wrap any exception into ValueError with a clear message
            raise ValueError(f"Failed to format entry for employee '{employee.name}': {exc}") from exc

    return "\n".join(formatted_entries)

# -------------------------------------------------------------
# Example usage (commented out – remove to run)
# -------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_team_roster("Engineering", tmpl))