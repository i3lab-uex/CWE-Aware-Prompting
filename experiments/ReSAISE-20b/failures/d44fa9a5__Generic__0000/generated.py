import re
from typing import Dict

# ------------------------------------------------------------------
# Dummy data models (replace with real implementations in your project)
# ------------------------------------------------------------------

class Employee:
    def __init__(self, worker_id: str, name: str, position: str):
        self.worker_id = worker_id
        self.name = name
        self.position = position


class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback  # Sensitive data
        self.bonus = bonus         # Sensitive data


# ------------------------------------------------------------------
# In‑memory registry (replace with database/API look‑ups)
# ------------------------------------------------------------------

EMPLOYEE_DB: Dict[str, Employee] = {
    "W001": Employee("W001", "Alice Smith", "Software Engineer"),
    "W002": Employee("W002", "Bob Johnson", "Product Manager"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "W001": Performance("Excellent", "Great work on the new feature.", 5000.00),
    "W002": Performance("Good", "Delivered the roadmap on time.", 3000.00),
}


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generates a performance report for the given worker using the provided template.

    The function replaces placeholders in the format `{worker.<field>}` and
    `{assessment.<field>}` with actual values. Allowed fields are:
        - worker.name
        - worker.position
        - assessment.rating

    Any attempt to access sensitive fields such as `feedback` or `bonus`
    will raise a ValueError.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the employee.
    template : str
        Report template containing placeholders.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the worker_id is unknown, or if the template contains
        disallowed placeholders.
    """

    # ------------------------------------------------------------------
    # Validation: worker existence
    # ------------------------------------------------------------------
    employee = EMPLOYEE_DB.get(worker_id)
    if not employee:
        raise ValueError(f"Worker ID '{worker_id}' does not exist.")

    performance = PERFORMANCE_DB.get(worker_id)
    if not performance:
        raise ValueError(f"No performance data for worker ID '{worker_id}'.")

    # ------------------------------------------------------------------
    # Find all placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(template)

    # ------------------------------------------------------------------
    # Mapping of allowed placeholders to actual values
    # ------------------------------------------------------------------
    mapping = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "assessment.rating": performance.rating,
    }

    # ------------------------------------------------------------------
    # Check for disallowed placeholders
    # ------------------------------------------------------------------
    disallowed = {"feedback", "bonus"}
    for ph in placeholders:
        if ph in disallowed:
            raise ValueError(f"Access to sensitive field '{ph}' is not allowed.")
        if ph not in mapping:
            raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # ------------------------------------------------------------------
    # Perform substitution safely
    # ------------------------------------------------------------------
    def replace(match):
        key = match.group(1)
        return mapping[key]

    result = placeholder_pattern.sub(replace, template)

    return result


# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Performance Rating: {assessment.rating}\n"
    )
    print(create_employee_report("W001", tmpl))