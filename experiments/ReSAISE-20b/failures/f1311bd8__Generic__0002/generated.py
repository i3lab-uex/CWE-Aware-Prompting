import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Data models (simplified for this example)
# --------------------------------------------------------------------

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
    # Restricted fields – should never be exposed through the template
    feedback: str = field(repr=False, default="")
    bonus: float = field(repr=False, default=0.0)

# --------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# --------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager",
                     department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work",
                        bonus=1200.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good",
                        bonus=800.0),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def get_employee(emp_id: str) -> Employee:
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with id '{emp_id}' not found") from exc

def get_performance(emp_id: str) -> Performance:
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee '{emp_id}' not found") from exc

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        The identifier of the employee.
    template_str : str
        A template string containing placeholders such as
        '{employee.name}', '{employee.position}',
        '{performance.rating}'. Restricted fields like
        'feedback' or 'bonus' are not allowed.

    Returns
    -------
    str
        The template string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if a
        restricted field is requested in the template.
    """
    employee = get_employee(emp_id)
    performance = get_performance(emp_id)

    # Allowed placeholders and their corresponding values
    allowed_values = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": str(performance.rating),
    }

    # Regex to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1)
        if key in allowed_values:
            return allowed_values[key]
        # Reject restricted or unknown fields
        raise ValueError(f"Access to '{key}' is not permitted in the report template")

    try:
        result = placeholder_pattern.sub(replace_placeholder, template_str)
    except ValueError as exc:
        raise

    return result