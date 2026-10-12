import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Dummy data store and helper functions (would normally be replaced by real   #
#  database access code).                                                      #
# --------------------------------------------------------------------------- #

class Employee:
    """Represents an employee."""
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    """Represents performance data for an employee."""
    def __init__(self, emp_id: str, rating: float, feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback      # Restricted field
        self.bonus = bonus            # Restricted field

# In-memory "database"
_EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

_PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent teamwork and coding skills.", 5000),
    "E002": Performance("E002", 4.0, "Strong leadership but needs to improve on deadlines.", 3000),
}

def _fetch_employee(emp_id: str) -> Employee:
    """Retrieve an employee instance from the data store."""
    emp = _EMPLOYEE_DB.get(emp_id)
    if not emp:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    return emp

def _fetch_performance(emp_id: str) -> Performance:
    """Retrieve a performance instance from the data store."""
    perf = _PERFORMANCE_DB.get(emp_id)
    if not perf:
        raise ValueError(f"Performance data for employee ID '{emp_id}' is missing.")
    return perf

# --------------------------------------------------------------------------- #
#  Core function implementation                                                #
# --------------------------------------------------------------------------- #

_RESTRICTED_FIELDS = {"feedback", "bonus"}

_PLACEHOLDER_REGEX = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*}")

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a formatted performance report for the given employee ID.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted report string with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template attempts to access a
        restricted field (e.g., 'feedback' or 'bonus').
    """
    # 1. Validate and fetch data
    employee = _fetch_employee(emp_id)
    performance = _fetch_performance(emp_id)

    # 2. Build a namespace for formatting
    context: Dict[str, Any] = {
        "employee": employee,
        "performance": performance,
    }

    # 3. Scan placeholders to detect restricted fields
    for match in _PLACEHOLDER_REGEX.finditer(report_template):
        field_path = match.group(1).split(".")
        if len(field_path) != 2:
            raise ValueError(f"Unsupported placeholder format: '{{{match.group(1)}}}'")
        scope, attr = field_path
        if attr in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed in reports.")

        # Ensure the attribute exists
        if scope not in context or not hasattr(context[scope], attr):
            raise ValueError(f"Field '{scope}.{attr}' does not exist for employee ID '{emp_id}'.")

    # 4. Perform the formatting safely
    try:
        report = report_template.format(**context)
    except Exception as exc:
        # Wrap any formatting errors to provide a clear message
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report