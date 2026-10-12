import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Dummy data structures (replace with your actual implementations)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    worker_id: str
    rating: float
    feedback: str   # Sensitive information
    bonus: float    # Sensitive information

# Sample in‑memory database (replace with real data source)
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, feedback="Excellent teamwork.", bonus=1200.00),
    "E002": Performance(worker_id="E002", rating=3.8, feedback="Strong leadership.", bonus=800.00),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _get_employee(worker_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[worker_id]
    except KeyError as exc:
        raise ValueError(f"Invalid worker ID: {worker_id}") from exc

def _get_performance(worker_id: str) -> Performance:
    """Retrieve a performance record by worker ID, raising ValueError if not found."""
    try:
        return PERFORMANCES[worker_id]
    except KeyError as exc:
        raise ValueError(f"No performance record for worker ID: {worker_id}") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a formatted performance report for the specified worker.

    Parameters
    ----------
    worker_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as `{worker.name}`,
        `{worker.position}`, and `{assessment.rating}`.

    Returns
    -------
    str
        The template string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the worker ID is invalid, or if the template contains
        unauthorized placeholders (`feedback` or `bonus`) or references
        non‑existent attributes.
    """
    # Validate worker existence
    employee = _get_employee(worker_id)
    performance = _get_performance(worker_id)

    # Define allowed placeholders and their corresponding values
    placeholder_map = {
        "worker.id": employee.id,
        "worker.name": employee.name,
        "worker.position": employee.position,
        "worker.department": employee.department,
        "assessment.rating": performance.rating,
    }

    # Unauthorized placeholders
    forbidden = {"feedback", "bonus"}

    # Find all placeholders in the template
    pattern = re.compile(r"\{([^{}]+)\}")
    matches = pattern.findall(template)

    for placeholder in matches:
        # Check for forbidden data
        if any(forbidden_word in placeholder.split(".")[-1] for forbidden_word in forbidden):
            raise ValueError(f"Unauthorized access to sensitive data via placeholder: {{{placeholder}}}")

        # Resolve nested attributes (e.g., worker.name)
        if placeholder not in placeholder_map:
            raise ValueError(f"Unknown placeholder: {{{placeholder}}}")

    # Perform the actual substitution
    def replacer(match):
        key = match.group(1)
        return str(placeholder_map[key])

    result = pattern.sub(replacer, template)
    return result

# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Department: {worker.department}\n"
        "Performance Rating: {assessment.rating}"
    )
    print(create_employee_report("E001", tmpl))