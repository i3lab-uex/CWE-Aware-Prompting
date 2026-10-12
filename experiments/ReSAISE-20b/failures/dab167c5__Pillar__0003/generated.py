import re
from dataclasses import dataclass, field
from typing import List

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    """Immutable representation of an employee."""
    name: str
    position: str
    department: str
    salary: float = field(repr=False)
    personal_email: str = field(repr=False)

# ----------------------------------------------------------------------
# Sample data store (in a real system this would come from a DB)
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee(name="Alice Smith", position="Engineer",
             department="Engineering", salary=95000.0,
             personal_email="alice.smith@example.com"),
    Employee(name="Bob Johnson", position="Manager",
             department="Engineering", salary=120000.0,
             personal_email="bob.johnson@example.com"),
    Employee(name="Carol Lee", position="HR Specialist",
             department="Human Resources", salary=70000.0,
             personal_email="carol.lee@example.com"),
    # ... more employees
]

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
PLACEHOLDER_REGEX = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Fields that are considered sensitive and must not be exposed
SENSITIVE_FIELDS = {"salary", "personal_email"}

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive employee fields.
    Raises ValueError if a prohibited field is found.
    """
    for match in PLACEHOLDER_REGEX.finditer(template):
        field_name = match.group(1)
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Template references sensitive data: '{field_name}'")

def _format_employee(employee: Employee, template: str) -> str:
    """
    Safely format a single employee instance using the provided template.
    The function replaces placeholders of the form {employee.field} with
    the corresponding attribute value.
    """
    # Build a mapping from placeholder names to values
    employee_dict = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department
    }

    # Replace placeholders in the template with actual values
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return str(employee_dict[key])

    return PLACEHOLDER_REGEX.sub(replacer, template)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted roster for all employees in the specified team.

    Parameters
    ----------
    team : str
        The department name whose employees will be included.
    template_str : str
        A string containing placeholders like {employee.name} that will be
        replaced with employee data.

    Returns
    -------
    str
        A multiline string where each line contains the formatted details of
        an employee belonging to the specified department.

    Raises
    ------
    ValueError
        If the template references sensitive data or if any other error occurs.
    """
    # 1. Validate the template against sensitive fields
    _validate_template(template_str)

    # 2. Filter employees by department (case‑insensitive match)
    selected = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
    if not selected:
        raise ValueError(f"No employees found for department '{team}'")

    # 3. Format each employee using the template
    try:
        formatted_lines = [_format_employee(e, template_str) for e in selected]
    except Exception as exc:
        # Any unexpected formatting issue should be surfaced as ValueError
        raise ValueError(f"Failed to format employee data: {exc}") from exc

    # 4. Join the lines into a single string
    return "\n".join(formatted_lines)

# ----------------------------------------------------------------------
# Example usage (commented out; remove the comments to run)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(create_team_roster("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")