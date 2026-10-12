import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Dummy data structures (in a real system these would come from a DB or
# an external service).  They are kept minimal for demonstration.
# --------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str
    position: str

@dataclass(frozen=True)
class Performance:
    employee_id: str
    rating: float
    feedback: str   # Sensitive, must not be exposed
    bonus: float    # Sensitive, must not be exposed

# --------------------------------------------------------------------
# In‑memory “database” of employees and performance records.
# --------------------------------------------------------------------
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent work on the recent project.", 5000),
    "E002": Performance("E002", 4.0, "Good leadership and communication.", 3000),
}

# --------------------------------------------------------------------
# Allowed placeholders in the template.  Anything else is considered
# sensitive or disallowed.
# --------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS = {
    "personnel.name",
    "personnel.position",
    "review.rating",
}

# Regular expression to find placeholders of the form {something}
_PLACEHOLDER_RE = re.compile(r"\{([^\{\}]+)\}")

def _validate_template(template: str) -> None:
    """
    Ensure that the template only contains allowed placeholders.
    Raises ValueError if a disallowed placeholder is found.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        key = match.group(1).strip()
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unauthorized placeholder '{key}' in template")

def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return _EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {employee_id}") from exc

def _get_performance(employee_id: str) -> Performance:
    """Retrieve a performance record by employee ID, raising ValueError if not found."""
    try:
        return _PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"No performance record for employee ID: {employee_id}") from exc

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee using the provided
    template.  The function only allows safe placeholders; any attempt to
    expose sensitive data (e.g., feedback or bonus) will raise ValueError.

    Parameters:
        employee_id: Unique identifier of the employee.
        template:   Template string containing placeholders.

    Returns:
        A formatted string with the placeholders replaced by actual data.

    Raises:
        ValueError: If the employee ID is invalid or if the template
                    contains disallowed placeholders.
    """
    # Validate template first to guard against CWE‑200
    _validate_template(template)

    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Build a mapping for safe placeholders
    values: Dict[str, str] = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "review.rating": f"{performance.rating:.1f}",
    }

    # Use a custom replacement function to avoid accidental format errors
    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        return values[key]

    result = _PLACEHOLDER_RE.sub(replacer, template)
    return result