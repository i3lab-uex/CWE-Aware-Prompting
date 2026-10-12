import re
from string import Formatter
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance

class Performance:
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Mock database of employees for illustration purposes.
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(rating=4.5, feedback="Great work!", bonus=1200)
    ),
    # Add more employees as needed...
}

# Restricted fields that should not be exposed in the report.
RESTRICTED_FIELDS = {"feedback", "bonus"}

# Allowed fields that can be used in the template.
ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating"
}

def _extract_placeholders(template: str):
    """
    Return a set of placeholder names found in the template.
    """
    formatter = Formatter()
    placeholders = set()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:  # ignore literal braces
            placeholders.add(field_name)
    return placeholders

def _build_context(employee: Employee):
    """
    Build a dictionary mapping placeholder names to actual values.
    """
    return {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": employee.performance.rating
    }

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the employee identified by `emp_id`
    using the provided `report_template`.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID is not found, or if the template references a
        restricted field.
    """
    # Retrieve employee record; raise error if not found
    employee = EMPLOYEE_DB.get(emp_id)
    if employee is None:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")

    # Parse template for placeholders
    placeholders = _extract_placeholders(report_template)

    # Check for restricted fields
    for placeholder in placeholders:
        if placeholder.split('.')[0] == 'performance' and placeholder.split('.')[-1] in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{placeholder}' is not allowed.")
        if placeholder not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown or disallowed placeholder '{placeholder}'.")

    # Build context for formatting
    context = _build_context(employee)

    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior checks, but guard anyway
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return report