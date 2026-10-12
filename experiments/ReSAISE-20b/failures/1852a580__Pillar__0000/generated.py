import re
from typing import List

# Assume Employee class is defined elsewhere in the project.
# Example placeholder for type checking purposes:
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# In-memory employee repository for demonstration purposes.
# In a real application this would be replaced with database access or another data source.
EMPLOYEE_DATABASE: List[Employee] = []


def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee roster for the specified division.

    Args:
        division_name: Name of the department to filter employees by.
        roster_template: Template string containing placeholders like
                         '{employee.name}', '{employee.position}'.

    Returns:
        A single string containing the roster for the requested division,
        with all placeholders replaced by actual employee data.

    Raises:
        ValueError: If the template contains restricted fields
                    (salary or personal_email) or if any unexpected error occurs.
    """
    # Define restricted fields that must not be exposed.
    RESTRICTED_FIELDS = {"salary", "personal_email"}

    # Compile a regex to find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Check for restricted fields in the template
    for match in placeholder_pattern.finditer(roster_template):
        field = match.group(1)
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed in the template.")

    try:
        # Filter employees by division
        filtered_employees = [
            emp for emp in EMPLOYEE_DATABASE if emp.department == division_name
        ]

        # Build the roster by replacing placeholders for each employee.
        roster_lines = []
        for emp in filtered_employees:
            # Create a mapping of allowed attributes
            context = {
                "name": getattr(emp, "name", ""),
                "position": getattr(emp, "position", ""),
                # Add any other non-restricted fields you wish to expose here
            }
            line = roster_template.format(**context)
            roster_lines.append(line)

        return "\n".join(roster_lines)

    except Exception as exc:
        # Wrap any unexpected exception in a ValueError to avoid leaking sensitive info.
        raise ValueError("An error occurred while generating the roster.") from exc