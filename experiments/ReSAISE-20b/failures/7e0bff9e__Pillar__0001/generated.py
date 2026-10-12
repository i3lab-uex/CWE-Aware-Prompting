import re
from typing import Any

# ----------------------------------------------------------------------
# Minimal context classes (for illustration; in real code these would be
# defined elsewhere and imported).
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str):
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, rating: float, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# ----------------------------------------------------------------------
# In‑memory "database" of employees and performances
# (In production this would be replaced by real persistence logic).
# ----------------------------------------------------------------------
EMPLOYEES = {
    "E001": Employee("Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("Bob Jones", "Product Manager", "Product"),
}

PERFORMANCES = {
    "E001": Performance(4.5, "Excellent work on project X.", 1200.0),
    "E002": Performance(3.8, "Good collaboration with cross‑team.", 900.0),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_code: str) -> Employee:
    """Retrieve an employee instance, raising ValueError if not found."""
    emp = EMPLOYEES.get(emp_code)
    if emp is None:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    return emp


def _get_performance(emp_code: str) -> Performance:
    """Retrieve a performance instance, raising ValueError if not found."""
    perf = PERFORMANCES.get(emp_code)
    if perf is None:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.")
    return perf


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a formatted performance report for an employee.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted performance report string.

    Raises
    ------
    ValueError
        If the employee or performance record is missing, or if a
        restricted field (feedback or bonus) is requested.
    """
    # Fetch data objects
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Define allowed placeholders
    ALLOWED_FIELDS = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Regex to find all placeholders of the form {<field>}
    placeholder_pattern = re.compile(r"{([^{}]+)}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if key in ("performance.feedback", "performance.bonus"):
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder '{key}'.")
        return str(ALLOWED_FIELDS[key])

    # Perform substitution
    try:
        report = placeholder_pattern.sub(replace_placeholder, summary_template)
    except ValueError as exc:
        raise

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Employee: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Rating: {performance.rating}"
#     )
#     print(create_performance_report("E001", template))