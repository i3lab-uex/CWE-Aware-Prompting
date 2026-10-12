import re
from typing import Dict, Any

# Assume these classes are defined elsewhere in the project.
try:
    from employee import Employee  # type: ignore
except ImportError:  # pragma: no cover
    # Minimal stubs for type checking / documentation purposes.
    class Employee:
        def __init__(self, emp_id: str):
            self.id = emp_id
            # Example attributes – in real code these would be populated from a DB.
            self.name = "John Doe"
            self.position = "Software Engineer"
            self.department = "Engineering"

        @staticmethod
        def get_by_id(emp_id: str) -> 'Employee':
            # Placeholder implementation – replace with real lookup logic.
            if emp_id == "invalid":
                raise KeyError
            return Employee(emp_id)

class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

    @staticmethod
    def get_by_employee(emp: Employee) -> 'Performance':
        # Placeholder implementation – replace with real lookup logic.
        return Performance(rating="Excellent", feedback="Great work!", bonus=5000.0)

# ---------------------------------------------------------------------------

ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

RESTRICTED_PLACEHOLDERS = {
    "employee.feedback",
    "performance.bonus",
}

PLACEHOLDER_PATTERN = re.compile(r"{([^}]+)}")

def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the specified employee using the given template.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the template references a restricted field or if `emp_id` is not found.
    """
    # 1. Validate template for restricted placeholders
    for match in PLACEHOLDER_PATTERN.finditer(report_template):
        placeholder = f"{match.group(1)}"
        if placeholder in RESTRICTED_PLACEHOLDERS:
            raise ValueError(f"Access to restricted field '{placeholder}' is not allowed.")

    # 2. Retrieve employee data
    try:
        employee = Employee.get_by_id(emp_id)
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.") from exc

    # 3. Retrieve performance data
    performance = Performance.get_by_employee(employee)

    # 4. Build mapping for allowed placeholders
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # 5. Validate that all placeholders in the template are allowed
    for match in PLACEHOLDER_PATTERN.finditer(report_template):
        placeholder = f"{match.group(1)}"
        if placeholder not in context:
            raise ValueError(f"Unknown placeholder '{placeholder}' in template.")

    # 6. Perform formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to previous checks, but guard anyway.
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return report