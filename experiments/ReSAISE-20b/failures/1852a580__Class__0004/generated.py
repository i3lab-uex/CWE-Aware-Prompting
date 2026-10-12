import re
from typing import List

# Assuming an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# For type checking purposes we define a minimal protocol here.
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# This list should be populated with Employee instances in the real application.
EMPLOYEES: List[Employee] = []

def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string template containing placeholders of the form `{employee.<field>}`.

    Returns
    -------
    str
        A string containing the roster, one formatted entry per line.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary or personal_email)
        or if an unexpected error occurs during processing.
    """
    # Fields that are not allowed to be exposed
    restricted_fields = {"salary", "personal_email"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = placeholder_pattern.findall(roster_template)

    # Validate that no restricted fields are used
    for field in placeholders:
        if field in restricted_fields:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")

    # Filter employees by division
    filtered_employees = [
        emp for emp in EMPLOYEES if getattr(emp, "department", None) == division_name
    ]

    # Build the roster string
    lines = []
    try:
        for emp in filtered_employees:
            # Create a mapping from field names to their string representations
            context = {field: str(getattr(emp, field)) for field in placeholders}

            # Replace each placeholder manually to avoid exposing restricted attributes
            def replace(match):
                field_name = match.group(1)
                return context.get(field_name, "")

            formatted_line = placeholder_pattern.sub(replace, roster_template)
            lines.append(formatted_line)

        return "\n".join(lines)

    except Exception as exc:
        # Any unexpected error is wrapped into a ValueError to satisfy the contract
        raise ValueError(f"An error occurred while generating the roster: {exc}") from exc