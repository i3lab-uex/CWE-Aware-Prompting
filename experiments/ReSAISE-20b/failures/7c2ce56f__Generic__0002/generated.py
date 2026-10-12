import re
from typing import Iterable, List

# The Employee class is assumed to be defined elsewhere in the codebase.
# It should have at least the following attributes:
#   - name: str
#   - position: str
#   - department: str
#   - salary: float (sensitive)
#   - personal_email: str (sensitive)
#
# Additionally, a global iterable `EMPLOYEES` containing all Employee instances
# should be available.  For example:
#
#   EMPLOYEES: Iterable[Employee] = [...]

SENSITIVE_FIELDS = {"salary", "personal_email"}


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not contain any placeholders for sensitive
    employee attributes.
    Raises ValueError if a sensitive placeholder is found.
    """
    # Find all occurrences of {employee.<attr>}
    pattern = r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    for match in re.finditer(pattern, template):
        attr = match.group(1)
        if attr in SENSITIVE_FIELDS:
            raise ValueError(
                f"Template contains sensitive attribute '{attr}'. "
                "Access to this field is prohibited."
            )


def _format_employee(employee, template: str) -> str:
    """
    Format a single employee's data into the provided template.
    Raises ValueError if formatting fails for any reason.
    """
    # Build a mapping of attributes
    mapping = {
        "name": getattr(employee, "name", ""),
        "position": getattr(employee, "position", ""),
        "department": getattr(employee, "department", ""),
    }

    try:
        return template.format(**mapping)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format employee '{employee.name}': {exc}") from exc


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Args:
        team: Department name used to filter employees.
        template_text: Directory template containing placeholders such as
                       '{employee.name}', '{employee.position}', etc.

    Returns:
        A string containing the formatted directory entries for all employees
        in the specified department, each entry separated by a newline.

    Raises:
        ValueError: If any placeholder refers to a sensitive attribute,
                    or if an error occurs during formatting.
    """
    # Validate the template once
    _validate_template(template_text)

    # Filter employees by department
    try:
        selected: List = [
            emp for emp in EMPLOYEES if getattr(emp, "department", "") == team
        ]
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to filter employees for team '{team}': {exc}") from exc

    # Format each employee
    formatted_entries = []
    for emp in selected:
        entry = _format_employee(emp, template_text)
        formatted_entries.append(entry)

    return "\n".join(formatted_entries)