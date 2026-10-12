import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Example data models (would normally be imported from the system)
# ------------------------------------------------------------------
@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    worker_id: str
    rating: float
    feedback: str   # Sensitive, must not be exposed
    bonus: float    # Sensitive, must not be exposed

# ------------------------------------------------------------------
# In‑memory "database" of employees and performances
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=1200.0),
    "E002": Performance(worker_id="E002", rating=3.8, feedback="Good leadership.", bonus=800.0),
}

# ------------------------------------------------------------------
# Allowed placeholder fields
# ------------------------------------------------------------------
ALLOWED_FIELDS = {
    "worker.name",
    "worker.position",
    "worker.department",
    "assessment.rating",
}

# ------------------------------------------------------------------
# Helper to extract placeholders from a template
# ------------------------------------------------------------------
_placeholder_pattern = re.compile(r"\{([^\}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _placeholder_pattern.finditer(template)}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker using the provided template.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders like {worker.name}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the worker_id is unknown, or if the template contains disallowed placeholders.
    """
    # Validate worker ID
    employee = EMPLOYEES.get(worker_id)
    if not employee:
        raise ValueError(f"Invalid worker ID: {worker_id}")

    performance = PERFORMANCES.get(worker_id)
    if not performance:
        raise ValueError(f"No performance data for worker ID: {worker_id}")

    # Validate placeholders
    placeholders = _extract_placeholders(template)
    for ph in placeholders:
        if ph not in ALLOWED_FIELDS:
            raise ValueError(f"Unauthorized placeholder '{ph}' used in template")

    # Build a mapping for safe formatting
    context = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": performance.rating,
    }

    # Perform substitution
    try:
        formatted = template.format(**context)
    except KeyError as exc:
        # Should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted