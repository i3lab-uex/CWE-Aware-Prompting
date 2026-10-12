import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Domain models (simplified for this example)
# --------------------------------------------------------------------

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

# --------------------------------------------------------------------
# In‑memory data store (replace with real DB access in production)
# --------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=1200.0),
    "E002": Performance(worker_id="E002", rating=4.2, feedback="Great leadership.", bonus=1100.0),
}

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def _get_employee(worker_id: str) -> Employee:
    try:
        return EMPLOYEES[worker_id]
    except KeyError as exc:
        raise ValueError(f"Invalid worker ID: {worker_id}") from exc

def _get_performance(worker_id: str) -> Performance:
    try:
        return PERFORMANCES[worker_id]
    except KeyError as exc:
        raise ValueError(f"No performance data for worker ID: {worker_id}") from exc

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the worker.
    template : str
        Template string containing placeholders such as {worker.name}
        and {assessment.rating}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the worker ID is invalid or if the template tries to access
        unauthorized fields (e.g., {assessment.feedback} or {assessment.bonus}).
    """
    # Retrieve data
    employee = _get_employee(worker_id)
    performance = _get_performance(worker_id)

    # Allowed placeholder patterns
    allowed_fields = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": f"{performance.rating:.1f}",
    }

    # Identify placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = set(placeholder_pattern.findall(template))

    # Check for unauthorized access
    forbidden_fields = {"assessment.feedback", "assessment.bonus"}
    if placeholders & forbidden_fields:
        raise ValueError(
            f"Unauthorized access to sensitive data: {placeholders & forbidden_fields}"
        )

    # Ensure all placeholders are known
    unknown_placeholders = placeholders - allowed_fields.keys()
    if unknown_placeholders:
        raise ValueError(f"Unknown placeholder(s) in template: {unknown_placeholders}")

    # Perform the substitution
    try:
        report = template.format(**allowed_fields)
    except KeyError as exc:
        # This should not happen due to the previous checks, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report