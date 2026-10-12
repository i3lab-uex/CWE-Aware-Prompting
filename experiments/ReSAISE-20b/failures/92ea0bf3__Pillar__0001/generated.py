import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Domain classes (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: str  # e.g. "Excellent", "Needs Improvement"
    feedback: str = field(repr=False)  # sensitive, not exposed
    bonus: float = field(repr=False)   # sensitive, not exposed


@dataclass
class Employee:
    name: str
    position: str
    department: str
    performance: Performance


# ----------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        name="Alice Johnson",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding leadership and technical skill.",
            bonus=12000.0,
        ),
    ),
    "E002": Employee(
        name="Bob Smith",
        position="Product Manager",
        department="Marketing",
        performance=Performance(
            rating="Satisfactory",
            feedback="Meets expectations but needs improvement in stakeholder communication.",
            bonus=8000.0,
        ),
    ),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{(?P<obj>\w+)\.(?P<attr>\w+)\}")


def _extract_placeholders(template: str):
    """Return a set of (obj, attr) tuples found in the template."""
    return {(m.group("obj"), m.group("attr")) for m in PLACEHOLDER_RE.finditer(template)}


def _validate_placeholders(placeholders):
    """Raise ValueError if restricted fields are requested."""
    for obj, attr in placeholders:
        # Disallow access to sensitive attributes
        if (obj == "performance" and attr in {"feedback", "bonus"}):
            raise ValueError(f"Access to restricted field '{obj}.{attr}' is not allowed.")
        # Disallow unknown objects
        if obj not in {"employee", "performance"}:
            raise ValueError(f"Unknown placeholder object '{obj}'.")


def _build_context(emp: Employee):
    """Return a dict suitable for format() that contains only allowed attributes."""
    ctx = {
        "employee": {
            "name": emp.name,
            "position": emp.position,
            "department": emp.department,
        },
        "performance": {
            "rating": emp.performance.rating,
        },
    }
    return ctx


def _safe_format(template: str, context: dict) -> str:
    """
    Perform a safe formatting of the template using the provided context.
    Raises KeyError if an unexpected placeholder is encountered.
    """
    # Convert nested dicts into flat mapping with dot notation
    flat_context = {}
    for obj, attrs in context.items():
        for attr, value in attrs.items():
            flat_context[f"{obj}.{attr}"] = value

    # Use a simple replacement loop to avoid str.format's potential pitfalls
    result = template
    for key, value in flat_context.items():
        result = result.replace(f"{{{key}}}", str(value))
    # After replacement, check if any unreplaced placeholders remain
    if PLACEHOLDER_RE.search(result):
        missing = _extract_placeholders(result)
        raise KeyError(f"Missing data for placeholders: {missing}")
    return result


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee does not exist, or if restricted fields are requested.
    KeyError
        If the template references a placeholder that cannot be resolved.
    """
    # 1. Retrieve employee
    try:
        emp = EMPLOYEES[emp_key]
    except KeyError as exc:
        raise ValueError(f"Employee with key '{emp_key}' not found.") from exc

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(template_str)
    _validate_placeholders(placeholders)

    # 3. Build context and format
    ctx = _build_context(emp)
    return _safe_format(template_str, ctx)


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Summary:\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(build_employee_summary("E001", template))