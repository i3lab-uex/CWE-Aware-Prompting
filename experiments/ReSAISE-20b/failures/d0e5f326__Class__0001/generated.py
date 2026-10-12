import re
from dataclasses import dataclass, field
from typing import Dict

# --- Data model ---------------------------------------------------------------

@dataclass(frozen=True)
class Employee:
    """Represents an employee."""
    id: str
    name: str
    department: str
    position: str

@dataclass(frozen=True)
class Performance:
    """Represents a performance evaluation."""
    employee_id: str
    rating: str
    feedback: str = field(repr=False)   # Sensitive data – do not expose
    bonus: float = field(repr=False)    # Sensitive data – do not expose

# --- In‑memory "database" ---------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", department="Engineering",
                     position="Senior Engineer"),
    "E002": Employee(id="E002", name="Bob Johnson", department="Marketing",
                     position="Manager"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating="Excellent",
                        feedback="Outstanding contribution to the project.",
                        bonus=5000.00),
    "E002": Performance(employee_id="E002", rating="Satisfactory",
                        feedback="Meets expectations in most areas.",
                        bonus=3000.00),
}

# --- Helper ---------------------------------------------------------------

ALLOWED_PLACEHOLDERS = {
    "staff.name",
    "staff.department",
    "staff.position",
    "evaluation.rating",
}

PLACEHOLDER_PATTERN = re.compile(r"{([^}]+)}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {m.group(1).strip() for m in PLACEHOLDER_PATTERN.finditer(template)}

def _build_context(employee: Employee, performance: Performance) -> Dict[str, str]:
    """Create a mapping of allowed placeholders to their string values."""
    return {
        "staff.name": employee.name,
        "staff.department": employee.department,
        "staff.position": employee.position,
        "evaluation.rating": performance.rating,
    }

# --- Public API -----------------------------------------------------------

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Generate a performance report for the given employee using the supplied
    template. The template may contain placeholders such as
    `{staff.name}`, `{staff.position}`, and `{evaluation.rating}`.

    Raises:
        ValueError: If the employee ID is unknown, or if the template
            contains disallowed placeholders (e.g. `{evaluation.feedback}`).
    """
    # Validate employee existence
    employee = EMPLOYEES.get(employee_id)
    if not employee:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    # Validate performance record
    performance = PERFORMANCES.get(employee_id)
    if not performance:
        raise ValueError(f"No performance record for employee ID: {employee_id}")

    # Detect placeholders
    placeholders = _extract_placeholders(template)
    disallowed = placeholders - ALLOWED_PLACEHOLDERS
    if disallowed:
        raise ValueError(f"Unauthorized placeholders in template: {sorted(disallowed)}")

    # Build context and format
    context = _build_context(employee, performance)
    try:
        report = template.format(**context)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing placeholder in context: {exc}") from exc

    return report