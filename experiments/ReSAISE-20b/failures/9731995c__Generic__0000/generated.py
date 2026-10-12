import re
from typing import Dict, Any

# Dummy data store for demonstration purposes.
EMPLOYEES = {
    "E001": {"name": "Alice Smith", "position": "Software Engineer", "department": "Engineering"},
    "E002": {"name": "Bob Johnson", "position": "Product Manager", "department": "Product"},
}

PERFORMANCES = {
    "E001": {"rating": 4.5, "feedback": "Excellent work on the new feature.", "bonus": 1200},
    "E002": {"rating": 3.8, "feedback": "Good progress on the roadmap.", "bonus": 800},
}


class Employee:
    def __init__(self, data: Dict[str, Any]):
        self.name = data["name"]
        self.position = data["position"]
        self.department = data["department"]


class Performance:
    def __init__(self, data: Dict[str, Any]):
        self.rating = data["rating"]
        # Sensitive fields are not exposed
        self._feedback = data["feedback"]
        self._bonus = data["bonus"]

    @property
    def feedback(self):
        raise ValueError("Access to sensitive information 'feedback' is not allowed.")

    @property
    def bonus(self):
        raise ValueError("Access to sensitive information 'bonus' is not allowed.")


# Allowed placeholders mapping
PLACEHOLDER_MAP = {
    "employee.name": lambda emp, perf: emp.name,
    "employee.position": lambda emp, perf: emp.position,
    "employee.department": lambda emp, perf: emp.department,
    "performance.rating": lambda emp, perf: f"{perf.rating:.1f}",
}


def _fetch_employee(employee_id: str) -> Employee:
    data = EMPLOYEES.get(employee_id)
    if not data:
        raise ValueError(f"Employee ID '{employee_id}' not found.")
    return Employee(data)


def _fetch_performance(employee_id: str) -> Performance:
    data = PERFORMANCES.get(employee_id)
    if not data:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")
    return Performance(data)


def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Args:
        employee_id (str): The ID of the employee.
        template (str): A string containing placeholders like
                        '{employee.name}', '{performance.rating}', etc.

    Returns:
        str: The generated summary string with placeholders replaced.

    Raises:
        ValueError: If an error occurs, if a placeholder references
                    sensitive data (feedback or bonus), or if the employee
                    or performance record cannot be found.
    """
    # Validate template placeholders
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    matches = placeholder_pattern.findall(template)

    # Fetch data once
    employee = _fetch_employee(employee_id)
    performance = _fetch_performance(employee_id)

    # Build the replacement dictionary
    replacements: Dict[str, str] = {}
    for key in matches:
        if key not in PLACEHOLDER_MAP:
            raise ValueError(f"Unsupported placeholder '{{{key}}}' in template.")
        # Compute the value
        try:
            value = PLACEHOLDER_MAP[key](employee, performance)
        except ValueError as exc:
            # Propagate sensitive access error
            raise ValueError(str(exc)) from None
        replacements[key] = str(value)

    # Replace placeholders safely
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))

    result = placeholder_pattern.sub(replacer, template)
    return result