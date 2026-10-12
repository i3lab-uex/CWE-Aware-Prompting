import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Mock data store (in a real system this would be replaced by
# database access or an external service)
# ------------------------------------------------------------------
class Employee:
    """Represents an employee."""
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    """Represents an employee's performance record."""
    def __init__(self, emp_id: str, rating: float,
                 feedback: str = None, bonus: float = 0.0):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


# Simple in‑memory store for demonstration purposes.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer",
                     "Engineering"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager",
                     "Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, feedback="Excellent work",
                        bonus=1200.0),
    "E002": Performance("E002", 3.8, feedback="Good leadership",
                        bonus=800.0),
}


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Create a performance summary for the specified employee.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    summary_template : str
        A template string containing placeholders such as
        '{employee.name}', '{performance.rating}'.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID does not exist, or if the template tries to
        access restricted fields (e.g., feedback, bonus).
    """
    # ------------------------------------------------------------------
    # 1. Validate employee existence
    # ------------------------------------------------------------------
    employee = EMPLOYEES.get(emp_id)
    performance = PERFORMANCES.get(emp_id)

    if employee is None or performance is None:
        raise ValueError(f"Invalid employee ID: {emp_id}")

    # ------------------------------------------------------------------
    # 2. Prepare a mapping of allowed placeholders
    # ------------------------------------------------------------------
    allowed_fields = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # ------------------------------------------------------------------
    # 3. Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(summary_template)

    # ------------------------------------------------------------------
    # 4. Validate each placeholder
    # ------------------------------------------------------------------
    for ph in placeholders:
        if ph not in allowed_fields:
            raise ValueError(f"Access to restricted or unknown field: "
                             f"{ph}")

    # ------------------------------------------------------------------
    # 5. Perform substitution safely
    # ------------------------------------------------------------------
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        return str(allowed_fields[key])

    result = placeholder_pattern.sub(replace_match, summary_template)

    return result


# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee {employee.name} ({employee.position}) in "
        "{employee.department} received a rating of "
        "{performance.rating}."
    )
    print(create_performance_summary("E001", template))