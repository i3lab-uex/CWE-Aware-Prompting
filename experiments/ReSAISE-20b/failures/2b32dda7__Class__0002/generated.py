import re
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Assume these classes and data retrieval function are defined elsewhere in
# the codebase. They are only represented here for completeness of this module.
# --------------------------------------------------------------------------- #

class Employee:
    """Represents an employee's basic information."""
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    """Represents an employee's performance data."""
    def __init__(self, emp_id: str, rating: float,
                 feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback          # Sensitive
        self.bonus = bonus                # Sensitive

# Dummy data store (replace with real database queries in production)
EMPLOYEE_DB = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager", "Operations"),
}

PERFORMANCE_DB = {
    "E001": Performance("E001", 4.5, "Excellent leadership", 12000),
    "E002": Performance("E002", 3.8, "Good coordination", 8000),
}

def get_employee_by_id(emp_id: str) -> Employee:
    """Retrieve an Employee object by ID."""
    employee = EMPLOYEE_DB.get(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    return employee

def get_performance_by_id(emp_id: str) -> Performance:
    """Retrieve a Performance object by ID."""
    performance = PERFORMANCE_DB.get(emp_id)
    if not performance:
        raise ValueError(f"Performance data for employee ID '{emp_id}' does not exist.")
    return performance

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating"
}

# Regex to capture placeholders like {employee.name}
PLACEHOLDER_RE = re.compile(r"{([^{}]+)}")

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance report for the specified employee using
    the provided template string.

    Parameters:
        emp_id (str): The unique identifier of the employee.
        report_template (str): Template containing placeholders.

    Returns:
        str: The formatted performance summary.

    Raises:
        ValueError: If the employee ID is invalid or if a
                    restricted field is accessed in the template.
    """
    # Validate employee existence
    employee = get_employee_by_id(emp_id)
    performance = get_performance_by_id(emp_id)

    # Build a mapping of allowed values
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating
    }

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_RE.findall(report_template)

    # Validate each placeholder
    for key in placeholders:
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown field '{key}' is not allowed."
            )

    # Perform safe substitution
    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1)
        return str(context[key])

    safe_report = PLACEHOLDER_RE.sub(replace_placeholder, report_template)
    return safe_report

# --------------------------------------------------------------------------- #
# Example usage (for testing only – remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee Report:\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    try:
        print(compile_performance_report("E001", template))
    except ValueError as exc:
        print(f"Error: {exc}")