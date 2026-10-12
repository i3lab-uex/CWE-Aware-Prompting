import re
from typing import List

# Assume a global list of Employee instances is available.
# In real usage this would be injected or fetched from a database.
EMPLOYEES: List["Employee"] = []  # type: ignore

class Employee:
    """
    Dummy implementation for context. In production this would be defined elsewhere.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Sensitive fields that must not be accessed through the template.
SENSITIVE_FIELDS = {"salary", "personal_email"}


def _extract_placeholders(template: str) -> List[str]:
    """
    Extract all placeholder names from the template.
    Example: "{employee.name} {employee.position}" -> ["name", "position"]
    """
    pattern = r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return re.findall(pattern, template)


def _format_employee(emp: Employee, placeholders: List[str]) -> str:
    """
    Format a single employee record according to the given placeholders.
    Raises ValueError if any sensitive field is requested or an attribute
    lookup fails.
    """
    values = {}
    for field in placeholders:
        if field in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is forbidden.")
        try:
            values[field] = getattr(emp, field)
        except AttributeError as exc:
            raise ValueError(f"Employee has no attribute '{field}'.") from exc

    # Build a string by replacing placeholders with actual values.
    result = template
    for field, value in values.items():
        placeholder = f"{{employee.{field}}}"
        result = result.replace(placeholder, str(value))
    return result


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Generate a directory string for all employees in the specified department.
    Each employee's details are formatted using `format_template`.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees.
    format_template : str
        Template containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The formatted directory listing.

    Raises
    ------
    ValueError
        If a sensitive field is referenced in the template or any other error
        occurs during formatting.
    """
    if not isinstance(dept_name, str) or not isinstance(format_template, str):
        raise ValueError("Both arguments must be strings.")

    # Extract placeholders once for efficiency.
    placeholders = _extract_placeholders(format_template)

    # Filter employees belonging to the requested department.
    dept_emps = [emp for emp in EMPLOYEES if emp.department == dept_name]

    # If no employees, return an empty string.
    if not dept_emps:
        return ""

    # Format each employee record safely.
    formatted_records = []
    for emp in dept_emps:
        try:
            formatted_records.append(_format_employee(emp, placeholders))
        except ValueError as exc:
            # Propagate the error with context.
            raise ValueError(f"Failed to format employee '{emp.name}': {exc}") from exc

    # Join records with newline separators.
    return "\n".join(formatted_records)