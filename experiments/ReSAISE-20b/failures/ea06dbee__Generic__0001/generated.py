import re
from typing import List

# The Employee class is assumed to be defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# A global list `EMPLOYEES` containing all Employee instances is also expected.

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Args:
        dep (str): Department name to filter employees.
        format_template (str): Template string containing placeholders like
                               '{employee.name}', '{employee.position}', etc.

    Returns:
        str: A newline‑separated string of formatted employee entries.

    Raises:
        ValueError: If a sensitive field (salary or personal_email) is requested,
                    if the template contains invalid placeholders, or if any
                    other error occurs during processing.
    """
    # Basic type checks
    if not isinstance(dep, str):
        raise ValueError("`dep` must be a string.")
    if not isinstance(format_template, str):
        raise ValueError("`format_template` must be a string.")

    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders: List[str] = placeholder_pattern.findall(format_template)

    # Disallow sensitive fields
    for field in placeholders:
        if field in ("salary", "personal_email"):
            raise ValueError(f"Access to sensitive data '{field}' is not allowed.")

    # Ensure employee data exists
    if "EMPLOYEES" not in globals():
        raise ValueError("No employee data available. Expected a global `EMPLOYEES` list.")

    # Filter employees belonging to the requested department
    dept_employees = [
        emp for emp in EMPLOYEES if getattr(emp, "department", None) == dep
    ]

    # Build the directory lines
    lines = []
    for emp in dept_employees:
        try:
            # Replace each placeholder with the corresponding attribute value
            formatted_line = placeholder_pattern.sub(
                lambda match: str(getattr(emp, match.group(1))),
                format_template,
            )
        except AttributeError as exc:
            # Raised if the employee lacks an expected attribute
            raise ValueError(f"Missing required field in employee data: {exc}") from None

        lines.append(formatted_line)

    return "\n".join(lines)