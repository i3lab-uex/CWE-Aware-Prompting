import re
from typing import Dict, Any

# Assume these classes are defined elsewhere in the system.
# They are imported here for type checking purposes only.
try:
    from company.models import Employee, Performance
except Exception:  # pragma: no cover
    # Minimal stubs for type checking / documentation.
    class Employee:
        def __init__(self, name: str, position: str, department: str):
            self.name = name
            self.position = position
            self.department = department

    class Performance:
        def __init__(self, rating: float):
            self.rating = rating

# Allowed placeholders (non‑sensitive)
_ALLOWED_PLACEHOLDERS: Dict[str, Any] = {
    "employee.name": lambda e, _: e.name,
    "employee.position": lambda e, _: e.position,
    "employee.department": lambda e, _: e.department,
    "performance.rating": lambda _, p: p.rating,
}

_PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")


def _get_employee(employee_id: str) -> Employee:
    """
    Retrieve an Employee instance by ID.
    This function should be replaced with the actual data access layer.
    """
    # Placeholder implementation – replace with real lookup logic.
    # For the purpose of this example we raise an error to signal missing implementation.
    raise NotImplementedError("Employee lookup not implemented.")


def _get_performance(employee: Employee) -> Performance:
    """
    Retrieve a Performance instance for the given employee.
    This function should be replaced with the actual data access layer.
    """
    # Placeholder implementation – replace with real lookup logic.
    raise NotImplementedError("Performance lookup not implemented.")


def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier for the employee.
    template : str
        A string containing placeholders to be replaced with actual data.

    Returns
    -------
    str
        The fully rendered summary string.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be retrieved,
        if a placeholder references sensitive information, or
        if the template contains an unsupported placeholder.
    """
    # Fetch employee and performance data safely.
    try:
        employee = _get_employee(employee_id)
        performance = _get_performance(employee)
    except Exception as exc:
        raise ValueError(f"Unable to retrieve data for employee '{employee_id}': {exc}") from exc

    # Find all placeholders in the template.
    placeholders = _PLACEHOLDER_PATTERN.findall(template)

    # Validate and resolve each placeholder.
    resolved_values: Dict[str, str] = {}
    for ph in placeholders:
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unsupported or sensitive placeholder detected: '{ph}'")
        try:
            value = _ALLOWED_PLACEHOLDERS[ph](employee, performance)
        except Exception as exc:
            raise ValueError(f"Error resolving placeholder '{ph}': {exc}") from exc
        resolved_values[ph] = str(value)

    # Perform the replacement.  We use a function to avoid partial replacements.
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return resolved_values.get(key, match.group(0))

    rendered_summary = _PLACEHOLDER_PATTERN.sub(replace_match, template)
    return rendered_summary