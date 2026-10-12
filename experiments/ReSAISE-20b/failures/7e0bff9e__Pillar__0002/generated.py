import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Assume the following classes are defined elsewhere in the system.
# They are included here only for type checking purposes.

class Employee:
    def __init__(self, name: str, position: str, department: str):
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback  # Restricted
        self.bonus = bonus        # Restricted

# ------------------------------------------------------------------
# Helper function to fetch employee and performance objects.
# In a real system these would be retrieved from a database or service.

def _get_employee(emp_code: str) -> Employee:
    # Placeholder implementation
    # Replace with actual data retrieval logic.
    return Employee(name="John Doe", position="Software Engineer", department="R&D")

def _get_performance(emp_code: str) -> Performance:
    # Placeholder implementation
    # Replace with actual data retrieval logic.
    return Performance(rating=4.5, feedback="Excellent teamwork", bonus=1200.0)

# ------------------------------------------------------------------
# Main function to create a performance report.

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a formatted performance report for an employee.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders like
        '{employee.name}', '{performance.rating}', etc.

    Returns
    -------
    str
        The template with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the template contains references to restricted fields
        (e.g., 'feedback', 'bonus') or if an unknown placeholder is used.
    """
    # Allowed placeholders
    allowed_fields = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating"
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = set(placeholder_pattern.findall(summary_template))

    # Validate placeholders
    for ph in placeholders:
        if ph not in allowed_fields:
            raise ValueError(f"Unauthorized or unknown placeholder: '{ph}'")

    # Retrieve data objects
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Build a dictionary for formatting
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating
    }

    # Perform safe formatting
    try:
        report = summary_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return report