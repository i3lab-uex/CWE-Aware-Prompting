import re
from typing import List

# Assuming an Employee class is defined elsewhere with the following attributes.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Placeholder: replace this with the actual data source in your application.
def get_all_employees() -> List[Employee]:
    """
    Return a list of all Employee instances.
    Replace the body with actual data retrieval logic (e.g., database query).
    """
    return []


def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A template string containing placeholders in the form
        '{employee.<field>}'.

    Returns
    -------
    str
        The formatted employee directory for the department.

    Raises
    ------
    ValueError
        If a restricted field is referenced in the template or an unexpected
        error occurs during formatting.
    """
    # Allowed fields that can be referenced in the template.
    ALLOWED_FIELDS = {"name", "position"}

    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = set(placeholder_pattern.findall(list_template))

    # Validate that all placeholders are allowed.
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Restricted or unknown field '{field}' used in template."
            )

    # Filter employees by department.
    all_employees = get_all_employees()
    dept_employees = [
        emp for emp in all_employees if emp.department == team_name
    ]

    # Build the formatted lines.
    formatted_lines = []
    for emp in dept_employees:
        try:
            # Create a mapping for formatting.
            mapping = {"employee": emp}
            line = list_template.format(**mapping)
        except Exception as exc:
            raise ValueError(
                f"Error formatting employee '{emp.name}': {exc}"
            ) from exc
        formatted_lines.append(line)

    return "\n".join(formatted_lines)