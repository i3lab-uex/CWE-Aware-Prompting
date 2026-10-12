import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data structures (normally provided by the system)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    # Sensitive data – should never be exposed through the report
    feedback: str
    bonus: float


# In a real system this would be loaded from a database or service.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        feedback="Excellent problem‑solving skills.",
        bonus=1200.0,
    ),
    "E002": Employee(
        id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        feedback="Strong leadership.",
        bonus=1500.0,
    ),
}


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the employee identified by `worker_id`
    using the provided `template`.

    The template may contain placeholders of the form `{worker.<field>}`.
    Only the following fields are allowed: name, position, department.

    Raises:
        ValueError: If `worker_id` is unknown or if the template tries to
                    access disallowed fields such as feedback or bonus.
    """
    # Retrieve the employee record
    worker = EMPLOYEES.get(worker_id)
    if worker is None:
        raise ValueError(f"Unknown worker ID: {worker_id}")

    # Allowed fields mapping
    allowed_fields = {
        "name": worker.name,
        "position": worker.position,
        "department": worker.department,
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    matches = placeholder_pattern.findall(template)

    for key in matches:
        # Expect format "worker.field"
        if not key.startswith("worker."):
            raise ValueError(f"Unsupported placeholder: {key}")

        field_name = key.split(".", 1)[1]
        if field_name not in allowed_fields:
            # Access to sensitive data is prohibited
            raise ValueError(f"Unauthorized access to field: {field_name}")

    # Perform the substitution safely
    def replacer(match):
        full_key = match.group(1)
        field_name = full_key.split(".", 1)[1]
        return allowed_fields[field_name]

    formatted_report = placeholder_pattern.sub(replacer, template)
    return formatted_report


# ----------------------------------------------------------------------
# Example usage (would normally be part of a test or separate script)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {worker.name}\n"
        "Position: {worker.position}\n"
        "Department: {worker.department}"
    )
    try:
        print(create_employee_report("E001", tmpl))
    except ValueError as exc:
        print(f"Error: {exc}")