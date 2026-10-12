import re
from typing import Dict

# Assuming these classes are defined elsewhere in the codebase.
# They should provide at least the attributes used below.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, performance):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance

class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Example in‑memory database of employees.
EMPLOYEE_DB: Dict[str, Employee] = {}

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee based on
    the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders in `{placeholder}` format.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee_id is not found, or if the template attempts to
        access unauthorized information (feedback or bonus).
    """
    # Verify employee exists
    employee = EMPLOYEE_DB.get(employee_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    # Build a safe mapping of allowed fields
    data_map = {
        "personnel.name": employee.name,
        "personnel.position": employee.position,
        "personnel.department": employee.department,
        "review.rating": employee.performance.rating,
    }

    # Detect unauthorized placeholders
    placeholders = re.findall(r"\{([^}]+)\}", template)
    for ph in placeholders:
        if ph.startswith("performance.") and ph not in data_map:
            raise ValueError(f"Unauthorized access to sensitive information: {ph}")

    # Replace placeholders
    try:
        summary = template.format(**data_map)
    except KeyError as e:
        raise ValueError(f"Unknown placeholder in template: {e.args[0]}") from e

    return summary