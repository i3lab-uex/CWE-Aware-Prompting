import string
from typing import List

# Assume an Employee class exists in the context with the following attributes:
# name, position, department, salary, personal_email
# The implementation below does not modify that class.

def build_team_directory(team: str, template_text: str) -> str:
    """
    Generate a formatted employee directory for the specified team.

    Args:
        team: The department name to filter employees.
        template_text: A string containing placeholders such as
                       '{employee.name}', '{employee.position}'.

    Returns:
        A string containing the formatted directory for all employees
        in the given department, each entry separated by a newline.

    Raises:
        ValueError: If the template tries to access sensitive
                    attributes (salary, personal_email) or if any other
                    error occurs during formatting.
    """
    # List of sensitive attributes that must not be exposed
    SENSITIVE_ATTRS = {"salary", "personal_email"}

    # Validate that the template does not reference sensitive data
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template_text):
        if not field_name:
            continue
        # Expect format like 'employee.attribute'
        parts = field_name.split(".")
        if len(parts) == 2 and parts[0] == "employee" and parts[1] in SENSITIVE_ATTRS:
            raise ValueError(f"Attempt to access sensitive attribute '{parts[1]}' in template")

    # Retrieve all employees from the global namespace
    try:
        employees: List[object] = [obj for obj in globals().values()
                                   if isinstance(obj, Employee) and getattr(obj, "department", None) == team]
    except Exception as exc:
        raise ValueError("Failed to retrieve employees") from exc

    if not employees:
        return ""

    # Build the directory
    formatted_entries = []
    for emp in employees:
        try:
            entry = template_text.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Error formatting entry for employee '{getattr(emp, 'name', '<unknown>')}'") from exc
        formatted_entries.append(entry)

    return "\n".join(formatted_entries)