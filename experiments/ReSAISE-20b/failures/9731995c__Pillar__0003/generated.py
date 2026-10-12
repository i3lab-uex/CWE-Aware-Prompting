import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Data models (simplified)
# ------------------------------------------------------------------

@dataclass
class Employee:
    employee_id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str   # Sensitive
    bonus: float    # Sensitive

# ------------------------------------------------------------------
# Simulated data store with context manager for safe access
# ------------------------------------------------------------------

_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager", "Marketing"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent leadership and coding.", 12000),
    "E002": Performance("E002", 3.8, "Good project delivery.", 8000),
}

@contextmanager
def employee_context():
    """
    Context manager that simulates safe access to the data store.
    In a real system this would open/close database connections or files.
    """
    try:
        yield
    finally:
        # In a real implementation, close connections/resources here.
        pass

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

_SENSITIVE_KEYS = {"performance.feedback", "performance.bonus"}

def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee by replacing placeholders
    in the provided template with actual data.

    Args:
        employee_id: The unique identifier of the employee.
        template: A string containing placeholders like
                  '{employee.name}', '{performance.rating}', etc.

    Returns:
        A formatted string with all placeholders replaced by data.

    Raises:
        ValueError: If the employee does not exist, a placeholder
                    refers to sensitive data, or an unknown key is used.
    """
    # 1. Validate template for sensitive placeholders
    if any(key in template for key in _SENSITIVE_KEYS):
        raise ValueError("Access to sensitive performance data is prohibited.")

    # 2. Retrieve employee and performance records safely
    with employee_context():
        employee = _EMPLOYEES.get(employee_id)
        performance = _PERFORMANCES.get(employee_id)

    if employee is None:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")
    if performance is None:
        raise ValueError(f"Performance record for employee '{employee_id}' not found.")

    # 3. Build a mapping of placeholder keys to values
    data_map = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": f"{performance.rating:.1f}",
    }

    # 4. Replace placeholders in the template
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        if key not in data_map:
            raise ValueError(f"Unknown placeholder '{{{key}}}' in template.")
        return data_map[key]

    pattern = re.compile(r"\{([^}]+)\}")
    try:
        result = pattern.sub(replacer, template)
    except re.error as exc:
        raise ValueError(f"Invalid template syntax: {exc}") from exc

    return result


# ------------------------------------------------------------------
# Example usage (for testing only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} in {employee.department}\n"
        "Rating: {performance.rating}"
    )
    print(generate_employee_summary("E001", tmpl))