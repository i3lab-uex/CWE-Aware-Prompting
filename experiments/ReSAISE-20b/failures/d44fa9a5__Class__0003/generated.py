import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mock data structures (in a real system these would be replaced by
# database models or external services)
# ------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    # Sensitive data (should never be exposed)
    feedback: str = field(repr=False, default="")
    bonus: float = field(repr=False, default=0.0)

@dataclass
class Performance:
    worker_id: str
    rating: float
    comments: str

# Sample in‑memory "database"
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Johnson",
        position="Software Engineer",
        department="R&D",
        feedback="Excellent problem‑solving skills.",
        bonus=5000.00,
    ),
    "E002": Employee(
        id="E002",
        name="Bob Smith",
        position="Product Manager",
        department="Marketing",
        feedback="Strong leadership.",
        bonus=7000.00,
    ),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(worker_id="E001", rating=4.5, comments="Consistently exceeds expectations."),
    "E002": Performance(worker_id="E002", rating=4.0, comments="Shows great initiative."),
}

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------

ALLOWED_PLACEHOLDERS = {
    "worker.name",
    "worker.position",
    "assessment.rating",
}

FORBIDDEN_SUBSTRINGS = {"feedback", "bonus"}

PLACEHOLDER_PATTERN = re.compile(r"\{([^\{\}]+)\}")

def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference any forbidden data.
    Raises ValueError if disallowed placeholders are found.
    """
    for match in PLACEHOLDER_PATTERN.finditer(template):
        key = match.group(1).strip()
        # Disallow any placeholder that contains forbidden substrings
        if any(fs in key for fs in FORBIDDEN_SUBSTRINGS):
            raise ValueError(f"Unauthorized placeholder detected: '{{{key}}}'")
        # Disallow any placeholder that is not in the allowed list
        if key not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unsupported placeholder: '{{{key}}}'")

def _replace_placeholders(template: str, context: Dict[str, any]) -> str:
    """
    Replace placeholders in the template using values from context.
    """
    def replacer(match):
        key = match.group(1).strip()
        return str(context.get(key, f"{{{key}}}"))
    return PLACEHOLDER_PATTERN.sub(replacer, template)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker using the supplied
    template. The function enforces that only non‑sensitive data may be
    accessed via placeholders.

    Parameters:
        worker_id (str): Unique identifier of the employee.
        template  (str): Template string containing placeholders.

    Returns:
        str: Formatted performance report.

    Raises:
        ValueError: If the worker ID is unknown, or if the template
                    references disallowed data.
    """
    # Validate worker existence
    employee = EMPLOYEES.get(worker_id)
    if not employee:
        raise ValueError(f"Unknown worker ID: {worker_id}")

    # Validate template safety
    _validate_template(template)

    # Build context for allowed placeholders
    performance = PERFORMANCES.get(worker_id)
    if not performance:
        raise ValueError(f"No performance record for worker ID: {worker_id}")

    context = {
        "worker.name": employee.name,
        "worker.position": employee.position,
        "assessment.rating": performance.rating,
    }

    # Perform replacement
    report = _replace_placeholders(template, context)
    return report

# ------------------------------------------------------------------
# Example usage (for testing purposes only)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report\n"
        "----------------\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Rating: {assessment.rating}\n"
    )
    print(create_employee_report("E001", tmpl))