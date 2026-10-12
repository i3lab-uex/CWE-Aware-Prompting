import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Sample data structures (would normally be provided by the system)
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
    feedback: str  # sensitive
    bonus: float   # sensitive

# ------------------------------------------------------------------
# In‑memory "database" of employees and performances
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(id="E002", name="Bob Jones", position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on the new feature.", bonus=1500.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good coordination with the team.", bonus=1200.0),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{emp_id}' not found.") from exc

def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance record by employee ID, raising ValueError if not found."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance record for employee ID '{emp_id}' not found.") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        The identifier of the employee.
    template_str : str
        Template string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance record does not exist, or if the template requests
        restricted fields like 'feedback' or 'bonus'.
    """
    # Validate placeholders to prevent exposure of sensitive data
    placeholder_pattern = re.compile(r"{([^}]+)}")
    placeholders = placeholder_pattern.findall(template_str)

    # Allowed fields
    allowed_fields = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating",
    }

    for ph in placeholders:
        if ph not in allowed_fields:
            raise ValueError(f"Unauthorized placeholder '{ph}' detected in template.")

    # Fetch data
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Build mapping for formatting
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Perform safe formatting
    try:
        report = template_str.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report