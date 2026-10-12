import re
from typing import Dict

# Assume these classes are defined elsewhere in the project.
class Employee:
    def __init__(self, code: str, name: str, position: str,
                 department: str):
        self.code = code
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee: Employee,
                 rating: str, feedback: str, bonus: float):
        self.employee = employee
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Dummy in‑memory data store for illustration purposes.
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Analyst",
                     "Finance"),
    "E002": Employee("E002", "Bob Johnson", "Developer",
                     "Engineering"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(EMPLOYEE_DB["E001"], "Excellent",
                        "Great leadership and teamwork.", 5000.0),
    "E002": Performance(EMPLOYEE_DB["E002"], "Good",
                        "Solid coding skills, needs improvement in documentation.",
                        3000.0),
}

# Allowed placeholders and their corresponding values
ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

# Forbidden placeholders
FORBIDDEN_PLACEHOLDERS = {
    "performance.feedback",
    "performance.bonus",
}


def _get_employee(emp_code: str) -> Employee:
    """Retrieve an employee instance by code."""
    emp = EMPLOYEE_DB.get(emp_code)
    if not emp:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    return emp


def _get_performance(emp: Employee) -> Performance:
    """Retrieve a performance instance for an employee."""
    perf = PERFORMANCE_DB.get(emp.code)
    if not perf:
        raise ValueError(f"Performance data for employee '{emp.code}' missing.")
    return perf


def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report for the given employee using the provided
    template string.

    Parameters:
        emp_code (str): Identifier of the employee.
        summary_template (str): Template containing placeholders.

    Returns:
        str: The formatted performance report.

    Raises:
        ValueError: If the employee or performance data is missing,
                    if a forbidden placeholder is used, or
                    if an unknown placeholder is encountered.
    """
    # Validate template placeholders
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    found_placeholders = set(placeholder_pattern.findall(summary_template))

    # Check for forbidden placeholders
    if FORBIDDEN_PLACEHOLDERS & found_placeholders:
        raise ValueError(
            f"Template contains restricted fields: "
            f"{', '.join(FORBIDDEN_PLACEHOLDERS & found_placeholders)}"
        )

    # Check for unknown placeholders
    allowed_and_forbidden = ALLOWED_PLACEHOLDERS | FORBIDDEN_PLACEHOLDERS
    unknown_placeholders = found_placeholders - allowed_and_forbidden
    if unknown_placeholders:
        raise ValueError(
            f"Template contains unsupported placeholders: "
            f"{', '.join(unknown_placeholders)}"
        )

    # Retrieve data
    employee = _get_employee(emp_code)
    performance = _get_performance(employee)

    # Map placeholders to actual values
    value_map: Dict[str, str] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Replace placeholders safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return value_map.get(key, "")

    report = placeholder_pattern.sub(_replace, summary_template)
    return report