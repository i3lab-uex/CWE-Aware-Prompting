import re
from typing import Dict

# --------------------------------------------------------------------
# Dummy data store – in a real system this would query a database
# --------------------------------------------------------------------
class Employee:
    """Represents an employee record."""
    def __init__(self, worker_id: str, name: str, position: str):
        self.worker_id = worker_id
        self.name = name
        self.position = position

class Performance:
    """Represents an employee's performance record."""
    def __init__(self, worker_id: str, rating: float,
                 feedback: str = "", bonus: float = 0.0):
        self.worker_id = worker_id
        self.rating = rating
        # The following fields are considered sensitive
        self.feedback = feedback
        self.bonus = bonus

# In‑memory "database"
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager"),
}
_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, feedback="Excellent teamwork.", bonus=1200),
    "E002": Performance("E002", 4.2, feedback="Strong leadership.", bonus=800),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _get_employee(worker_id: str) -> Employee:
    """Retrieve an employee by ID or raise ValueError."""
    emp = _EMPLOYEES.get(worker_id)
    if not emp:
        raise ValueError(f"Worker ID '{worker_id}' is invalid.")
    return emp

def _get_performance(worker_id: str) -> Performance:
    """Retrieve a performance record by ID or raise ValueError."""
    perf = _PERFORMANCES.get(worker_id)
    if not perf:
        raise ValueError(f"No performance record for worker ID '{worker_id}'.")
    return perf

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker ID by replacing
    placeholders in the provided template.

    Allowed placeholders:
        {worker.name}
        {worker.position}
        {assessment.rating}

    Any attempt to access sensitive data such as {assessment.feedback}
    or {assessment.bonus} will raise a ValueError.

    Parameters
    ----------
    worker_id : str
        Unique identifier for the employee.
    template : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the worker ID is invalid or if an unauthorized placeholder is used.
    """
    employee = _get_employee(worker_id)
    performance = _get_performance(worker_id)

    # Regex to find all placeholders like {worker.name}
    placeholder_pattern = re.compile(r"\{([a-zA-Z_]+)\.([a-zA-Z_]+)\}")

    def _replacement(match: re.Match) -> str:
        obj_name, attr = match.group(1), match.group(2)

        if obj_name == "worker":
            # Allowed attributes
            if attr in {"name", "position"}:
                return getattr(employee, attr)
        elif obj_name == "assessment":
            # Only rating is permitted
            if attr == "rating":
                return str(performance.rating)
        # If we reach here, the placeholder is unauthorized
        raise ValueError(f"Unauthorized access to '{obj_name}.{attr}'")

    # Perform replacement
    try:
        result = placeholder_pattern.sub(_replacement, template)
    except ValueError as exc:
        raise

    return result


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = ("Employee Report:\n"
            "Name: {worker.name}\n"
            "Position: {worker.position}\n"
            "Rating: {assessment.rating}\n")
    print(create_employee_report("E001", tmpl))