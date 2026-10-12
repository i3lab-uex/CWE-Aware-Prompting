import re
from typing import List

# Assuming an Employee class exists somewhere in the codebase.
# Here we define a minimal stub for type checking; replace with the real class as needed.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of employees – replace with the actual data source.
EMPLOYEES: List[Employee] = []

# Allowed fields that can be referenced in the template.
ALLOWED_FIELDS = {"name", "position", "department"}

# Regex to capture placeholder patterns like {employee.name}
PLACEHOLDER_RE = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_template(template: str) -> None:
    """
    Ensure that the template only contains allowed employee fields.
    Raises ValueError if a restricted field is used or an unexpected placeholder format appears.
    """
    for match in PLACEHOLDER_RE.finditer(template):
        field = match.group(1)
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Template contains restricted or unknown field: '{field}'. "
                "Allowed fields are: name, position, department."
            )

def _apply_template(employee: Employee, template: str) -> str:
    """
    Replace placeholders in the template with actual employee data.
    """
    def repl(match):
        field = match.group(1)
        return str(getattr(employee, field))
    return PLACEHOLDER_RE.sub(repl, template)

def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        Concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If restricted fields are referenced in the template or an unexpected error occurs.
    """
    try:
        # Validate template before processing
        _validate_template(roster_template)

        # Filter employees by department (case-insensitive match)
        filtered = [
            emp for emp in EMPLOYEES
            if emp.department.lower() == division_name.strip().lower()
        ]

        # Apply template to each employee
        formatted_entries = [_apply_template(emp, roster_template) for emp in filtered]

        # Join with newline separators; adjust as needed
        return "\n".join(formatted_entries)

    except ValueError:
        # Re-raise ValueErrors to signal template issues
        raise
    except Exception as exc:
        # Wrap any other exception in ValueError to conform to the spec
        raise ValueError(f"An error occurred while generating roster: {exc}") from exc