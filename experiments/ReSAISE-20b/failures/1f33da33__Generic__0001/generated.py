import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Mock data structures – in a real system these would be imported
# from the company's data layer.  They are kept simple here for
# demonstration purposes.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, emp_id: str, rating: float, feedback: str, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# ------------------------------------------------------------------
# Sample data – replace with actual persistence or service calls
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager", "Operations"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent leadership.", 5000),
    "E002": Performance("E002", 3.8, "Good teamwork.", 3000),
}


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee using the supplied template.

    Args:
        emp_id: The unique identifier of the employee.
        summary_template: A format string that may contain placeholders such as
                          '{employee.name}', '{performance.rating}', etc.

    Returns:
        A formatted string with placeholders replaced by actual values.

    Raises:
        ValueError: If the employee ID is unknown, or if the template attempts
                    to access restricted fields (feedback or bonus).
    """
    # ------------------------------------------------------------------
    # 1. Validate employee existence
    # ------------------------------------------------------------------
    employee = EMPLOYEES.get(emp_id)
    performance = PERFORMANCES.get(emp_id)

    if employee is None or performance is None:
        raise ValueError(f"Unknown employee ID: {emp_id}")

    # ------------------------------------------------------------------
    # 2. Parse placeholders and check for restricted fields
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{([^}]+)}")
    placeholders = placeholder_pattern.findall(summary_template)

    restricted_keys = {"feedback", "bonus"}
    for key in placeholders:
        # Keys may contain a dot, e.g., 'performance.feedback'
        base_key = key.split(".")[1] if "." in key else key
        if base_key.lower() in restricted_keys:
            raise ValueError(f"Access to restricted field '{base_key}' is not allowed.")

    # ------------------------------------------------------------------
    # 3. Build a mapping for formatting
    # ------------------------------------------------------------------
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # ------------------------------------------------------------------
    # 4. Perform formatting safely
    # ------------------------------------------------------------------
    try:
        formatted = summary_template.format(**context)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise ValueError(f"Template references unknown placeholder: {missing_key}") from None

    return formatted


# ------------------------------------------------------------------
# Example usage (would normally be part of unit tests or application logic)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee {employee.name} ({employee.position}) in {employee.department} "
        "received a rating of {performance.rating} this year."
    )
    print(create_performance_summary("E001", template))