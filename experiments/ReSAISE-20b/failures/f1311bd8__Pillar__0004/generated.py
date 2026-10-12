import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy data structures – in a real system these would come from a database
# --------------------------------------------------------------------------- #

class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, feedback: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.feedback = feedback  # restricted field


class Performance:
    def __init__(self, emp_id: str, rating: float, bonus: float):
        self.emp_id = emp_id
        self.rating = rating
        self.bonus = bonus  # restricted field


# In-memory mock database
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Engineer",
                     "R&D", "Excellent problem solving."),
    "E002": Employee("E002", "Bob Johnson", "Manager",
                     "Sales", "Strong leadership."),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, 5000.0),
    "E002": Performance("E002", 4.2, 3000.0),
}


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee instance. Raise ValueError if not found."""
    emp = EMPLOYEE_DB.get(emp_id)
    if emp is None:
        raise ValueError(f"Employee with ID {emp_id!r} not found.")
    return emp


def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance instance. Raise ValueError if not found."""
    perf = PERFORMANCE_DB.get(emp_id)
    if perf is None:
        raise ValueError(f"Performance record for ID {emp_id!r} not found.")
    return perf


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted performance report for the specified employee.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}',
        '{employee.position}', and '{performance.rating}'.

    Returns
    -------
    str
        The fully formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance record does not exist, or if the
        template references restricted fields (feedback or bonus).
    """
    # Retrieve data once; no persistent resources are held.
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Mapping of allowed placeholders to actual values
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Regex to find all placeholders of the form {key}
    placeholder_pattern = re.compile(r"{([^{}]+)}")

    def _replace(match: re.Match) -> str:
        key = match.group(1).strip()
        if key in ("employee.feedback", "performance.bonus"):
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        if key not in context:
            raise ValueError(f"Unknown placeholder '{key}' in template.")
        return str(context[key])

    # Perform substitution safely
    try:
        report = placeholder_pattern.sub(_replace, template_str)
    except ValueError as exc:
        raise  # re‑raise to propagate

    return report


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report\n"
        "---------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}\n"
    )
    print(create_employee_report("E001", tmpl))