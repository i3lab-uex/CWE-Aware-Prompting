import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Minimal in‑memory data store (for demonstration purposes)
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
        self.feedback = feedback          # Restricted field
        self.bonus = bonus                # Restricted field


# Sample data store
_EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
}

_PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent problem solving.", 5000),
    "E002": Performance("E002", 3.8, "Good communication.", 3000),
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"{(?P<field>[^}]+)}")
RESTRICTED_FIELDS = {"performance.feedback", "performance.bonus"}


def _build_context(emp_id: str) -> Dict[str, Any]:
    """Builds a dictionary of allowed fields for formatting."""
    employee = _EMPLOYEE_DB.get(emp_id)
    performance = _PERFORMANCE_DB.get(emp_id)

    if not employee or not performance:
        raise ValueError(f"Invalid employee ID: {emp_id}")

    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }
    return context


def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the specified employee.

    Args:
        emp_id: The unique identifier of the employee.
        summary_template: A template string containing placeholders.

    Returns:
        The formatted performance summary string.

    Raises:
        ValueError: If the employee ID is invalid or if restricted fields are
                    accessed in the template.
    """
    # Verify that no restricted fields appear in the template
    for match in PLACEHOLDER_PATTERN.finditer(summary_template):
        field = match.group("field")
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")

    context = _build_context(emp_id)

    # Perform safe replacement
    def replacer(match: re.Match) -> str:
        field = match.group("field")
        if field not in context:
            raise ValueError(f"Unknown placeholder '{field}' in template.")
        return str(context[field])

    try:
        result = PLACEHOLDER_PATTERN.sub(replacer, summary_template)
    except re.error as exc:
        raise ValueError(f"Invalid template: {exc}") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = (
#         "Employee: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}"
#     )
#     print(create_performance_summary("E001", tmpl))