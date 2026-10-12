import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Mocked data structures (replace with the real ones in your project)
# ------------------------------------------------------------------

@dataclass
class Employee:
    employee_id: str
    name: str
    department: str
    position: str


@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str
    bonus: float


# Example in‑memory repositories (replace with DB access in production)
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Engineering", "Senior Engineer"),
    "E002": Employee("E002", "Bob Johnson", "Marketing", "Marketing Lead"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent teamwork and delivery.", 1200.0),
    "E002": Performance("E002", 3.8, "Strong campaign results.", 800.0),
}


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee by substituting
    placeholders in ``template`` with data from Employee and Performance objects.

    Allowed placeholders:
        {personnel.name}
        {personnel.department}
        {personnel.position}
        {review.rating}

    Unallowed placeholders (e.g. feedback or bonus) will raise ValueError.

    Args:
        employee_id: Unique identifier of the employee.
        template: String containing placeholders to be replaced.

    Returns:
        A fully formatted string with all allowed placeholders substituted.

    Raises:
        ValueError: If the employee_id is unknown or if the template contains
                    unauthorized placeholders.
    """
    # Validate existence of employee and performance records
    if employee_id not in EMPLOYEES:
        raise ValueError(f"Unknown employee ID: {employee_id}")

    if employee_id not in PERFORMANCES:
        raise ValueError(f"No performance data for employee ID: {employee_id}")

    employee = EMPLOYEES[employee_id]
    performance = PERFORMANCES[employee_id]

    # Build a mapping of allowed placeholder names to values
    context = {
        "personnel.name": employee.name,
        "personnel.department": employee.department,
        "personnel.position": employee.position,
        "review.rating": performance.rating,
    }

    # Detect any placeholder that is not allowed
    # We use a regex to find all `{...}` patterns.
    placeholders = re.findall(r"{([^{}]+)}", template)
    for ph in placeholders:
        if ph not in context:
            # Disallow sensitive data or unknown keys
            raise ValueError(f"Unauthorized placeholder '{ph}' in template")

    # Perform safe substitution
    try:
        result = template.format(**context)
    except KeyError as exc:
        # This should not happen because we checked keys beforehand
        raise ValueError(f"Missing key in context: {exc}") from exc

    return result


# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee: {personnel.name}\n"
        "Department: {personnel.department}\n"
        "Position: {personnel.position}\n"
        "Performance Rating: {review.rating}"
    )
    print(compile_employee_evaluation("E001", tmpl))