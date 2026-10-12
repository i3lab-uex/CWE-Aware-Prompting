import re
from typing import List

# Assuming an Employee class exists in the context.
# If it doesn't, this placeholder is only for type checking purposes.
class Employee:
    name: str
    position: str
    department: str
    salary: float  # restricted
    personal_email: str  # restricted

# List of all employees in the system.
# In a real application this would be replaced with a database query or similar data source.
EMPLOYEES: List[Employee] = []  # populated elsewhere


def _replace_placeholders(template: str, employee: Employee) -> str:
    """
    Replace placeholders of the form `{employee.<field>}` in *template* with
    the corresponding attribute from *employee*. Raises ValueError if a
    restricted field is requested or an unknown placeholder is found.
    """
    # Allowed fields that can be used in the template
    allowed_fields = {"name", "position", "department"}

    # Find all placeholders in the template
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    matches = pattern.findall(template)

    # Validate all placeholders
    for field in matches:
        if field not in allowed_fields:
            raise ValueError(
                f"Access to restricted or unknown employee field '{field}' is not allowed."
            )

    # Perform the substitution
    def _replacer(match):
        field_name = match.group(1)
        return str(getattr(employee, field_name))

    return pattern.sub(_replacer, template)


def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The name of the department to filter employees by.
    roster_template : str
        A string template containing placeholders such as `{employee.name}`.

    Returns
    -------
    str
        A formatted string with each employee's details on a separate line.

    Raises
    ------
    ValueError
        If the template tries to access restricted fields (salary or personal_email)
        or if an unexpected error occurs during processing.
    """
    try:
        # Filter employees belonging to the requested division
        department_employees = [
            emp for emp in EMPLOYEES if emp.department == division_name
        ]

        # Build the roster string line by line
        lines = []
        for emp in department_employees:
            line = _replace_placeholders(roster_template, emp)
            lines.append(line)

        return "\n".join(lines)

    except ValueError as ve:
        # Propagate ValueErrors raised by placeholder replacement
        raise

    except Exception as exc:  # pragma: no cover
        # Catch-all for unexpected runtime errors
        raise ValueError(f"An error occurred while generating the roster: {exc}") from exc