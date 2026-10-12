import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data models (in a real system these would be imported from elsewhere)
# ----------------------------------------------------------------------
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
    feedback: str  # sensitive
    bonus: float   # sensitive

# ----------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, feedback="Excellent work on project X.", bonus=1200.0),
    "E002": Performance(worker_id="E002", rating=3.8, feedback="Good leadership.", bonus=800.0),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
UNAUTHORIZED_FIELDS = {"feedback", "bonus"}

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholders found in the template."""
    return set(re.findall(r"\{([^{}]+)\}", template))

def _validate_placeholders(placeholders: set) -> None:
    """Raise ValueError if any placeholder is unauthorized."""
    for ph in placeholders:
        # Only the first part of the path matters (e.g., worker.feedback)
        key = ph.split(".")[0]
        if key in UNAUTHORIZED_FIELDS:
            raise ValueError(f"Unauthorized access to sensitive field: {ph}")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a formatted employee performance report.

    Args:
        worker_id: Unique identifier of the employee.
        template: A string containing placeholders such as
                  '{worker.name}', '{worker.position}',
                  '{assessment.rating}'.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the worker ID is invalid or if the template
                    attempts to access sensitive data.
    """
    # Validate placeholders for security
    placeholders = _extract_placeholders(template)
    _validate_placeholders(placeholders)

    # Retrieve employee and performance data
    employee = EMPLOYEES.get(worker_id)
    if not employee:
        raise ValueError(f"Invalid worker ID: {worker_id}")

    performance = PERFORMANCES.get(worker_id)
    if not performance:
        raise ValueError(f"No performance data for worker ID: {worker_id}")

    # Build mapping for formatting
    mapping = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": performance.rating,
    }

    # Format the template
    try:
        report = template.format(**mapping)
    except KeyError as exc:
        # If the template contains an unknown placeholder
        raise ValueError(f"Unknown placeholder in template: {exc}") from None

    return report