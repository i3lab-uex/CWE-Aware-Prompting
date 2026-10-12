import re
from dataclasses import dataclass
from typing import Optional

# --------------------------------------------------------------------------- #
# Mocked data structures and repository for demonstration purposes.
# In a real system these would be replaced with actual database models
# and data access layers.

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: Optional[str] = None  # Sensitive data not exposed via template
    bonus: Optional[float] = None   # Sensitive data not exposed via template

# Simple in-memory "database"
_EMPLOYEES = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

_PERFORMANCES = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on the project.", bonus=5000),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership.", bonus=3000),
}

def _get_employee_by_id(employee_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    emp = _EMPLOYEES.get(employee_id)
    if not emp:
        raise ValueError(f"Employee ID '{employee_id}' is invalid.")
    return emp

def _get_performance_by_employee(employee: Employee) -> Performance:
    """Retrieve performance data for an employee, raising ValueError if not found."""
    perf = _PERFORMANCES.get(employee.id)
    if not perf:
        raise ValueError(f"Performance data for employee ID '{employee.id}' is missing.")
    return perf

# --------------------------------------------------------------------------- #
# Core function implementation.

_ALLOWED_PLACEHOLDERS = {
    "personnel.name",
    "personnel.position",
    "review.rating",
}

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a formatted employee evaluation summary.

    Parameters
    ----------
    employee_id : str
        Unique identifier for the employee.
    template : str
        Template string containing placeholders in the form '{placeholder}'.

    Returns
    -------
    str
        The formatted summary string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee ID is invalid, required data is missing,
        or an unauthorized placeholder is present in the template.
    """
    # Fetch employee and performance data
    employee = _get_employee_by_id(employee_id)
    performance = _get_performance_by_employee(employee)

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^}]+)}")
    placeholders = set(placeholder_pattern.findall(template))

    # Verify that all placeholders are allowed
    unauthorized = placeholders - _ALLOWED_PLACEHOLDERS
    if unauthorized:
        raise ValueError(f"Unauthorized placeholders detected: {', '.join(sorted(unauthorized))}")

    # Prepare a mapping from placeholder to actual value
    substitution_map = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "review.rating": f"{performance.rating:.1f}",
    }

    # Perform safe substitution
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return substitution_map.get(key, "")

    result = placeholder_pattern.sub(_replace, template)
    return result

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove or comment out in production)

if __name__ == "__main__":
    tmpl = (
        "Employee Evaluation Report\n"
        "Name: {personnel.name}\n"
        "Position: {personnel.position}\n"
        "Rating: {review.rating}/5\n"
    )
    print(compile_employee_evaluation("E001", tmpl))