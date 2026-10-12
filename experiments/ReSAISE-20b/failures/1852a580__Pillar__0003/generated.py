import re
from dataclasses import dataclass
from typing import List

# --------------------------------------------------------------------------- #
# Employee data model (minimal implementation for demonstration)
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# --------------------------------------------------------------------------- #
# Sample data source – in a real system this would be replaced by a DB call
# --------------------------------------------------------------------------- #
def get_all_employees() -> List[Employee]:
    """
    Returns a list of all employees. In production this would query a database.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice@example.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob@example.com"),
        Employee("Carol White", "HR Specialist", "Human Resources", 70000.0, "carol@example.com"),
    ]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generates a formatted employee roster for the specified department.

    Parameters
    ----------
    division_name : str
        The name of the department to filter employees by.
    roster_template : str
        A string template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted roster, with one line per employee.

    Raises
    ------
    ValueError
        If the template contains restricted fields (salary or personal_email)
        or if an unexpected error occurs during processing.
    """
    # Restricted attributes that must not be exposed
    RESTRICTED_FIELDS = {"salary", "personal_email"}

    # Compile regex to find placeholders of the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Validate template for restricted fields
    try:
        for match in placeholder_pattern.finditer(roster_template):
            field_name = match.group(1)
            if field_name in RESTRICTED_FIELDS:
                raise ValueError(
                    f"Template contains restricted field '{field_name}'. "
                    "Access to this data is prohibited."
                )
    except re.error as exc:
        # Regex compilation error
        raise ValueError(f"Invalid template syntax: {exc}") from exc

    # Retrieve employees and filter by department
    try:
        all_employees = get_all_employees()
        filtered = [
            emp for emp in all_employees if emp.department.lower() == division_name.lower()
        ]
    except Exception as exc:
        raise ValueError(f"Failed to retrieve employees: {exc}") from exc

    # If no employees found, return an empty string
    if not filtered:
        return ""

    # Build the roster string
    try:
        lines = []
        for emp in filtered:
            # Prepare a mapping that only exposes allowed attributes
            context = {
                "name": emp.name,
                "position": emp.position,
                # Add more safe fields here if needed
            }
            # Replace placeholders manually to avoid eval/format pitfalls
            line = roster_template
            for match in placeholder_pattern.finditer(roster_template):
                field_name = match.group(1)
                value = context.get(field_name, "")
                # Escape braces in the replacement to avoid nested formatting
                line = line.replace(match.group(0), str(value))
            lines.append(line)
        return "\n".join(lines)
    except Exception as exc:
        raise ValueError(f"Failed to generate roster: {exc}") from exc