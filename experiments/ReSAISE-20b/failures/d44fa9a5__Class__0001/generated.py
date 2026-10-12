import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Mocked data structures (in a real system these would be replaced by ORM models)
# --------------------------------------------------------------------------- #

@dataclass
class Performance:
    rating: str
    feedback: str = field(repr=False)  # sensitive, hidden from repr
    bonus: float = field(default=0.0, repr=False)  # sensitive

@dataclass
class Employee:
    worker_id: str
    name: str
    position: str
    department: str
    performance: Performance

# --------------------------------------------------------------------------- #
# Sample in‑memory "database" of employees (replace with real persistence)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        worker_id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(rating="Excellent", feedback="Great teamwork.", bonus=1200.00),
    ),
    "E002": Employee(
        worker_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(rating="Good", feedback="Needs to improve stakeholder communication.", bonus=800.00),
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

# Allowed placeholders in the template
ALLOWED_PLACEHOLDERS = {
    "worker.name",
    "worker.position",
    "worker.department",
    "assessment.rating",
}

# Regex to extract placeholder names from the template
PLACEHOLDER_REGEX = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_REGEX.finditer(template)}

def _build_context(employee: Employee) -> Dict[str, str]:
    """Build a mapping for safe template formatting."""
    return {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": employee.performance.rating,
    }

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker based on the provided template.

    Parameters
    ----------
    worker_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as `{worker.name}` or `{assessment.rating}`.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the worker ID is not found, or if the template attempts to access sensitive data
        (e.g., `{worker.feedback}` or `{assessment.bonus}`).
    """
    # Validate worker ID
    employee = EMPLOYEES.get(worker_id)
    if not employee:
        raise ValueError(f"Invalid worker ID: {worker_id}")

    # Detect placeholders
    placeholders = _extract_placeholders(template)

    # Check for disallowed sensitive placeholders
    forbidden = {"worker.feedback", "assessment.bonus"}
    if any(p in forbidden for p in placeholders):
        raise ValueError("Template contains unauthorized sensitive information")

    # Ensure all placeholders are allowed
    if not placeholders.issubset(ALLOWED_PLACEHOLDERS):
        unknown = placeholders - ALLOWED_PLACEHOLDERS
        raise ValueError(f"Template contains unsupported placeholder(s): {', '.join(sorted(unknown))}")

    # Build context and format the template
    context = _build_context(employee)
    try:
        report = template.format(**context)
    except KeyError as exc:
        # Should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing placeholder in context: {exc}") from exc

    return report