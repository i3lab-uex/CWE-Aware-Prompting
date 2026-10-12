import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Dummy data models (would normally be provided by the application)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str  # Restricted field
    bonus: float   # Restricted field

# ------------------------------------------------------------------
# In‑memory "database" for demonstration purposes
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Jones", position="Product Manager", department="Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent teamwork.", bonus=5000),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership.", bonus=3000),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' does not exist.") from exc

def _get_performance(employee_id: str) -> Performance:
    """Retrieve performance data for an employee, raising ValueError if not found."""
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{employee_id}' is missing.") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Generate a formatted performance report for the given employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the template references restricted fields or unknown placeholders,
        or if the employee ID is invalid.
    """
    # Define allowed placeholder namespaces and fields
    ALLOWED_FIELDS = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating"
    }

    # Regex to capture all placeholder names (non‑greedy)
    placeholders = set(re.findall(r"{([^{}]+)}", report_template))

    # Validate placeholders
    for ph in placeholders:
        if ph not in ALLOWED_FIELDS:
            raise ValueError(f"Restricted or unknown placeholder '{ph}' detected in template.")

    # Fetch data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Build mapping for format()
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating
    }

    # Perform formatting safely (no arbitrary code execution)
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report