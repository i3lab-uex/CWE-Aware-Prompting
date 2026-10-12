import re
from typing import List

# ----------------------------------------------------------------------
# Assuming an Employee class is defined elsewhere with the following
# attributes: name, position, department, salary, personal_email.
#
# For demonstration purposes we create a minimal Employee dataclass here.
# In real usage replace this with the actual implementation.

class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global list of employees – in real code this would come from
# a database or another module.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob.johnson@example.com"),
    Employee("Carol Lee", "Designer", "Design", 80000, "carol.lee@example.com"),
]

# ----------------------------------------------------------------------
# Function to build a team directory
# ----------------------------------------------------------------------


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted directory for all employees in the specified team.

    Parameters
    ----------
    team : str
        The department name to filter employees by.
    template_text : str
        A string containing placeholders such as '{employee.name}' or
        '{employee.position}'.  Only non‑sensitive attributes may be used.

    Returns
    -------
    str
        The concatenated directory entries, each entry on a new line.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive attributes (salary or
        personal_email) or if any other error occurs during formatting.
    """
    # Regular expression to capture all placeholder names inside braces
    placeholder_pattern = r"{([^}]+)}"
    placeholders = set(re.findall(placeholder_pattern, template_text))

    # Define the set of attributes that are considered sensitive
    SENSITIVE_ATTRIBUTES = {"salary", "personal_email"}

    # If any placeholder references a sensitive attribute, abort
    if placeholders & SENSITIVE_ATTRIBUTES:
        raise ValueError(
            f"Attempt to access sensitive attributes: {placeholders & SENSITIVE_ATTRIBUTES}"
        )

    # Build the directory for employees in the requested team
    entries: List[str] = []

    for employee in EMPLOYEES:
        if getattr(employee, "department", None) != team:
            continue

        try:
            # Format the template with the current employee instance
            entry = template_text.format(employee=employee)
        except Exception as exc:
            # Wrap any formatting exception into a ValueError for consistency
            raise ValueError(f"Failed to format entry: {exc}") from exc

        entries.append(entry)

    return "\n".join(entries)