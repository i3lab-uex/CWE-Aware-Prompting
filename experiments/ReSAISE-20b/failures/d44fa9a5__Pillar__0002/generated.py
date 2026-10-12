import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str  # not exposed in the report


@dataclass
class Performance:
    rating: float
    feedback: str   # not exposed in the report
    bonus: float    # not exposed in the report


# ----------------------------------------------------------------------
# In‑memory "database" of employees and performances
# ----------------------------------------------------------------------
EMPLOYEES = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Jones", position="Manager", department="Sales"),
}

PERFORMANCES = {
    "E001": Performance(rating=4.5, feedback="Excellent teamwork", bonus=1200),
    "E002": Performance(rating=3.8, feedback="Good leadership", bonus=800),
}


# ----------------------------------------------------------------------
# Helper: fetch data by worker_id
# ----------------------------------------------------------------------
def _get_worker_and_assessment(worker_id: str):
    """Retrieve Employee and Performance objects for a given worker ID."""
    employee = EMPLOYEES.get(worker_id)
    performance = PERFORMANCES.get(worker_id)

    if employee is None or performance is None:
        raise ValueError(f"Invalid worker ID: {worker_id}")

    return employee, performance


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the specified worker.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the worker.
    template : str
        Template string containing placeholders such as {worker.name},
        {worker.position}, and {assessment.rating}.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the worker ID is invalid or if the template contains
        placeholders that are not allowed (e.g., {assessment.feedback}).
    """
    # Retrieve data
    employee, performance = _get_worker_and_assessment(worker_id)

    # Allowed placeholders mapping
    allowed_placeholders = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "assessment.rating": performance.rating,
    }

    # Find all placeholders in the template
    placeholders = re.findall(r"\{([^{}]+)\}", template)

    # Validate placeholders
    for ph in placeholders:
        if ph not in allowed_placeholders:
            raise ValueError(f"Unauthorized placeholder detected: {{{ph}}}")

    # Safely format the template
    try:
        result = template.format(**allowed_placeholders)
    except KeyError as exc:
        # This should never happen because we validated placeholders
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Rating: {assessment.rating}"
    )
    print(create_employee_report("E001", tmpl))