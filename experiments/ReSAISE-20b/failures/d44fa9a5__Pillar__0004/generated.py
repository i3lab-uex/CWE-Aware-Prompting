import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Sample data structures (normally provided by the system)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str   # sensitive, should not be exposed via template
    bonus: float    # sensitive, should not be exposed via template

# ------------------------------------------------------------------
# In‑memory "database" of employees and performances
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on the project.", bonus=1200.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership skills.", bonus=950.0),
}

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generates a performance report for the specified worker by replacing
    placeholders in the template with actual data.

    Args:
        worker_id: Unique identifier of the worker.
        template: String containing placeholders like {worker.name}.

    Returns:
        A fully formatted report string.

    Raises:
        ValueError: If the worker_id is unknown, or if the template contains
                    placeholders for unauthorized data (e.g., feedback or bonus).
    """
    # Retrieve the employee and performance records
    employee = EMPLOYEES.get(worker_id)
    if not employee:
        raise ValueError(f"Invalid worker ID: {worker_id}")

    performance = PERFORMANCES.get(worker_id)
    if not performance:
        raise ValueError(f"No performance record found for worker ID: {worker_id}")

    # Allowed placeholder mapping
    allowed_placeholders = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "assessment.rating": str(performance.rating),
    }

    # Regular expression to find placeholders of the form {key}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if key in allowed_placeholders:
            return allowed_placeholders[key]
        # Disallow any placeholder that could expose sensitive data
        if key.startswith("worker.") or key.startswith("assessment."):
            # Unknown or unauthorized placeholder
            raise ValueError(f"Unauthorized or unknown placeholder: {{{key}}}")
        # If the placeholder doesn't match known patterns, raise error
        raise ValueError(f"Invalid placeholder: {{{key}}}")

    # Perform substitution safely
    try:
        result = placeholder_pattern.sub(replace_placeholder, template)
    except ValueError as ve:
        # Re‑raise to caller
        raise

    return result

# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Rating: {assessment.rating}/5\n"
    )
    print(create_employee_report("E001", tmpl))