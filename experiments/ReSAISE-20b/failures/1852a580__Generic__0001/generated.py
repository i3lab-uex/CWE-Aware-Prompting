import re
from typing import List

# Assume an Employee class is defined elsewhere in the codebase.
# Here we provide a minimal placeholder for type checking purposes only.
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# Global list of employees (should be populated elsewhere)
EMPLOYEES: List[Employee] = []

# Set of fields that are not allowed to be accessed via the template
RESTRICTED_FIELDS = {"salary", "personal_email"}

# Regex pattern to find placeholders like {employee.name}
PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

def _evaluate_placeholder(placeholder: str, employee: Employee) -> str:
    """
    Evaluate a single placeholder against an employee instance.
    Raises ValueError if the placeholder refers to a restricted field or is malformed.
    """
    # Expect format like "employee.name" or nested attributes e.g., "employee.address.city"
    parts = placeholder.split(".")
    if not parts or parts[0] != "employee":
        raise ValueError(f"Invalid placeholder: {{{placeholder}}}")

    # Check for restricted fields
    if parts[1] in RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted field '{parts[1]}' is not allowed")

    # Resolve the attribute chain
    value = employee
    for attr in parts[1:]:
        if not hasattr(value, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on {value}")
        value = getattr(value, attr)

    return str(value)


def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        A formatted string representing the employee directory for the specified department.

    Raises
    ------
    ValueError
        If a placeholder references a restricted field, an unknown attribute,
        or any unexpected error occurs during processing.
    """
    # Filter employees belonging to the requested division
    filtered_employees = [e for e in EMPLOYEES if e.department == division_name]

    # If no employees found, return an empty string
    if not filtered_employees:
        return ""

    rendered_lines = []

    try:
        for employee in filtered_employees:
            # Replace all placeholders in the template for this employee
            def replacer(match: re.Match) -> str:
                placeholder = match.group(1)
                return _evaluate_placeholder(placeholder, employee)

            rendered_line = PLACEHOLDER_PATTERN.sub(replacer, roster_template)
            rendered_lines.append(rendered_line)

    except Exception as exc:
        # Wrap any unexpected exception in ValueError with a clear message
        raise ValueError(f"Failed to generate roster: {exc}") from exc

    # Join all rendered lines with a newline separator
    return "\n".join(rendered_lines)