import re
from typing import List, Any

# Assume an Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float   (sensitive)
# personal_email: str  (sensitive)

# For the purpose of this function, we assume a global list `EMPLOYEES` exists.
# In real usage, this could be passed in or accessed via a database query.

SENSITIVE_FIELDS = {"salary", "personal_email"}
PLACEHOLDER_PATTERN = re.compile(r"{([^{}]+)}")


def _check_template_safety(template: str) -> None:
    """
    Raise ValueError if the template contains placeholders for sensitive fields.
    """
    for match in PLACEHOLDER_PATTERN.finditer(template):
        field = match.group(1).strip()
        # Allow nested attributes like employee.name
        if "." in field:
            attr = field.split(".")[-1]
        else:
            attr = field
        if attr in SENSITIVE_FIELDS:
            raise ValueError(f"Template contains sensitive placeholder '{field}'.")


def _format_employee(emp: Any, template: str) -> str:
    """
    Format a single employee record using the given template.
    Only non-sensitive attributes are allowed; accessing others will raise ValueError.
    """
    try:
        # Build a simple namespace dictionary for formatting
        ns = {
            "name": getattr(emp, "name", ""),
            "position": getattr(emp, "position", ""),
            "department": getattr(emp, "department", ""),
        }
        # Support nested syntax like {employee.name} if needed
        result = template.format(**ns)
        return result
    except KeyError as exc:
        raise ValueError(f"Missing attribute for placeholder: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Error formatting employee: {exc}") from exc


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the specified team using the provided template.

    Args:
        team: Department name to filter employees.
        template_text: Template string containing placeholders like '{name}' or
                       '{position}'. Sensitive fields such as 'salary' and
                       'personal_email' are not allowed.

    Returns:
        A single string containing the formatted directory for all employees
        in the specified team, separated by newlines.

    Raises:
        ValueError: If a sensitive field is accessed or any other error occurs.
    """
    # Ensure the template does not request sensitive data
    _check_template_safety(template_text)

    if team is None or not isinstance(team, str):
        raise ValueError("Team must be a non-empty string.")

    # Filter employees by department
    try:
        team_employees = [
            emp for emp in EMPLOYEES if getattr(emp, "department", None) == team
        ]
    except Exception as exc:
        raise ValueError(f"Error accessing employee data: {exc}") from exc

    if not team_employees:
        return ""

    # Format each employee and join with newlines
    try:
        formatted_lines = [_format_employee(emp, template_text) for emp in team_employees]
    except Exception as exc:
        raise ValueError(f"Error formatting employees: {exc}") from exc

    return "\n".join(formatted_lines)