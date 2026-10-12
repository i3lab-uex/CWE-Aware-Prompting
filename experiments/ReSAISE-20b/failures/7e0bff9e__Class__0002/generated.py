import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Dummy data structures (in a real system these would be fetched from
# a database or an external service)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    code: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_code: str
    rating: float
    feedback: str   # sensitive field
    bonus: float    # sensitive field

# Mock repositories -----------------------------------------------
EMPLOYEES_DB: Dict[str, Employee] = {
    "E001": Employee(code="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(code="E002", name="Bob Jones", position="Project Manager", department="Operations"),
}

PERFORMANCES_DB: Dict[str, Performance] = {
    "E001": Performance(employee_code="E001", rating=4.5, feedback="Excellent leadership.", bonus=5000),
    "E002": Performance(employee_code="E002", rating=3.8, feedback="Good coordination.", bonus=3000),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_code: str) -> Employee:
    try:
        return EMPLOYEES_DB[emp_code]
    except KeyError as exc:
        raise ValueError(f"Employee with code '{emp_code}' not found.") from exc

def _get_performance(emp_code: str) -> Performance:
    try:
        return PERFORMANCES_DB[emp_code]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee '{emp_code}' not found.") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Build a performance report for the employee identified by *emp_code*,
    using the provided *summary_template*. The template may contain
    placeholders of the form {employee.field} or {performance.field}.
    Restricted fields (feedback, bonus) are not allowed and will raise
    ValueError.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if a
        restricted field is requested in the template.
    """
    # Validate that the employee exists
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(summary_template)

    # Map allowed fields to their values
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Check for restricted fields
    for ph in placeholders:
        if ph not in context:
            # If the placeholder references a restricted field
            if ph.startswith("performance.") and ph.split(".", 1)[1] in {"feedback", "bonus"}:
                raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
            # If the placeholder references an unknown attribute
            raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # Perform the substitution safely
    def replace_match(match):
        key = match.group(1)
        return str(context[key])

    formatted_report = placeholder_pattern.sub(replace_match, summary_template)

    return formatted_report