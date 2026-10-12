import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model (minimal implementation for demonstration)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    name: str
    position: str
    department: str
    # Restricted fields that should not be exposed in templates
    feedback: str = ""
    bonus: float = 0.0


@dataclass
class Performance:
    rating: str
    comments: str
    # Restricted field
    bonus: float = 0.0


# --------------------------------------------------------------------------- #
# In‑memory data store (replace with real persistence in production)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        feedback="Excellent teamwork and problem solving.",
        bonus=1200.00,
    ),
    "E002": Employee(
        name="Bob Johnson",
        position="Product Manager",
        department="Marketing",
        feedback="Strong leadership skills.",
        bonus=950.00,
    ),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(
        rating="Outstanding",
        comments="Exceeded all quarterly targets.",
        bonus=1500.00,
    ),
    "E002": Performance(
        rating="Exceeds Expectations",
        comments="Delivered product launch on schedule.",
        bonus=1100.00,
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

_REPLACE_PATTERN = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

_ALLOWED_EMPLOYEE_FIELDS = {f.name for f in fields(Employee) if f.name not in {"feedback", "bonus"}}
_ALLOWED_PERFORMANCE_FIELDS = {f.name for f in fields(Performance) if f.name not in {"bonus"}}


def _extract_placeholders(template: str):
    """Return a set of placeholder keys found in the template."""
    return {match.group(1) for match in _REPLACE_PATTERN.finditer(template)}


def _validate_placeholders(placeholders: set):
    """Ensure placeholders reference only allowed fields."""
    for key in placeholders:
        if "." not in key:
            raise ValueError(f"Invalid placeholder '{key}'. Expected format 'object.field'.")
        obj, field = key.split(".", 1)
        if obj == "employee" and field not in _ALLOWED_EMPLOYEE_FIELDS:
            raise ValueError(f"Access to restricted or unknown employee field '{field}'.")
        if obj == "performance" and field not in _ALLOWED_PERFORMANCE_FIELDS:
            raise ValueError(f"Access to restricted or unknown performance field '{field}'.")
        if obj not in {"employee", "performance"}:
            raise ValueError(f"Unknown object '{obj}' in placeholder.")


def _build_context(emp: Employee, perf: Performance):
    """Create a dictionary that can be used with str.format."""
    context = {
        "employee": {f: getattr(emp, f) for f in _ALLOWED_EMPLOYEE_FIELDS},
        "performance": {f: getattr(perf, f) for f in _ALLOWED_PERFORMANCE_FIELDS},
    }
    # Flatten nested dicts so that {employee.name} works
    flat_context = {}
    for obj_name, attrs in context.items():
        for attr_name, value in attrs.items():
            flat_context[f"{obj_name}.{attr_name}"] = value
    return flat_context


# --------------------------------------------------------------------------- #
# Main function to implement
# --------------------------------------------------------------------------- #

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier for the employee (e.g., "E001").
    template_str : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee key is unknown, or if restricted fields are requested,
        or if placeholders refer to unknown attributes.
    """
    # Retrieve data
    employee = EMPLOYEES.get(emp_key)
    if not employee:
        raise ValueError(f"Employee with key '{emp_key}' not found.")
    performance = PERFORMANCES.get(emp_key)
    if not performance:
        raise ValueError(f"Performance data for employee '{emp_key}' not found.")

    # Validate placeholders
    placeholders = _extract_placeholders(template_str)
    _validate_placeholders(placeholders)

    # Build context for formatting
    context = _build_context(employee, performance)

    try:
        return template_str.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = (
#         "Employee: {employee.name} ({employee.position})\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}\n"
#         "Comments: {performance.comments}"
#     )
#     print(build_employee_summary("E001", tmpl))