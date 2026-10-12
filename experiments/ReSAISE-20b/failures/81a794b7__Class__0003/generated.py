import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Dummy data structures and in‑memory store
# ------------------------------------------------------------------

@dataclass
class Performance:
    rating: str          # e.g. "Excellent", "Needs Improvement"
    feedback: str        # Sensitive: should not be exposed
    bonus: float         # Sensitive: should not be exposed

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    performance: Performance

# In‑memory employee database (for demonstration purposes)
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        position="Software Engineer",
        department="Engineering",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding performance on project X.",
            bonus=1500.00
        )
    ),
    "E002": Employee(
        id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(
            rating="Meets Expectations",
            feedback="Good collaboration with teams.",
            bonus=800.00
        )
    ),
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"{([^}]+)}")

ALLOWED_FIELDS = {
    "personnel.name",
    "personnel.position",
    "review.rating"
}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the specified employee based on
    the provided template.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders such as
        '{personnel.name}', '{personnel.position}', or '{review.rating}'.

    Returns
    -------
    str
        The formatted performance summary with placeholders replaced.

    Raises
    ------
    ValueError
        If the employee_id is not found or if the template contains an
        unauthorized placeholder (e.g., accessing feedback or bonus).
    """
    # Validate employee existence
    employee = EMPLOYEE_DB.get(employee_id)
    if not employee:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_PATTERN.findall(template)

    # Build a mapping from placeholder to value
    substitution: Dict[str, str] = {}
    for ph in placeholders:
        # Enforce allowed fields only
        if ph not in ALLOWED_FIELDS:
            raise ValueError(f"Unauthorized placeholder detected: {{{ph}}}")

        # Resolve the value based on known fields
        if ph == "personnel.name":
            substitution[ph] = employee.name
        elif ph == "personnel.position":
            substitution[ph] = employee.position
        elif ph == "review.rating":
            substitution[ph] = employee.performance.rating
        else:
            # This branch should never be reached due to the ALLOWED_FIELDS check
            raise ValueError(f"Unhandled placeholder: {{{ph}}}")

    # Replace placeholders safely
    def replace(match):
        key = match.group(1)
        return substitution.get(key, "")

    result = PLACEHOLDER_PATTERN.sub(replace, template)
    return result

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {personnel.name}\n"
        "Position: {personnel.position}\n"
        "Performance Rating: {review.rating}"
    )
    print(compile_employee_evaluation("E001", tmpl))