import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy data structures – in a real system these would come from a database
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    id: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    worker_id: str
    rating: float
    feedback: str   # Sensitive information
    bonus: float    # Sensitive information


# In‑memory “database” of employees and their performance records
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=1200.0),
    "E002": Performance(worker_id="E002", rating=3.8, feedback="Good team leadership.", bonus=800.0),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _get_employee(worker_id: str) -> Employee:
    """Retrieve an employee or raise ValueError if not found."""
    try:
        return EMPLOYEES[worker_id]
    except KeyError as exc:
        raise ValueError(f"Invalid worker ID: {worker_id}") from exc


def _get_performance(worker_id: str) -> Performance:
    """Retrieve a performance record or raise ValueError if not found."""
    try:
        return PERFORMANCES[worker_id]
    except KeyError as exc:
        raise ValueError(f"No performance record for worker ID: {worker_id}") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker by substituting
    placeholders in *template* with the corresponding employee data.

    Allowed placeholders (case‑sensitive):
        {worker.name}
        {worker.position}
        {performance.rating}

    Any attempt to access sensitive data such as feedback or bonus will
    raise a ValueError.  The function also raises ValueError if the worker_id
    is unknown or no performance record exists.

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
    """
    # Validate inputs
    if not isinstance(worker_id, str) or not worker_id:
        raise ValueError("worker_id must be a non-empty string")
    if not isinstance(template, str):
        raise ValueError("template must be a string")

    # Retrieve data
    employee = _get_employee(worker_id)
    performance = _get_performance(worker_id)

    # Build a mapping of allowed keys to their values
    context = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "performance.rating": performance.rating,
    }

    # Find all placeholders in the template
    placeholder_pattern = r"\{([^{}]+)\}"
    placeholders = re.findall(placeholder_pattern, template)

    # Validate that each placeholder is allowed
    for key in placeholders:
        if key not in context:
            # Check for sensitive keys explicitly
            if key.startswith("performance.feedback") or key.startswith("performance.bonus"):
                raise ValueError(f"Unauthorized access to sensitive data: {key}")
            else:
                raise ValueError(f"Unknown placeholder in template: {key}")

    # Perform substitution safely
    def replace(match):
        key = match.group(1)
        return str(context[key])

    result = re.sub(r"\{([^{}]+)\}", replace, template)
    return result


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Rating: {performance.rating}"
    )
    print(create_employee_report("E001", tmpl))