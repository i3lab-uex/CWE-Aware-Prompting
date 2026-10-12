import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Domain models
# ------------------------------------------------------------------

@dataclass
class Employee:
    """Represents an employee record."""
    id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents a performance evaluation record."""
    employee_id: str
    rating: float
    feedback: str = field(repr=False)   # Sensitive: hidden in repr
    bonus: float = field(repr=False)     # Sensitive: hidden in repr


# ------------------------------------------------------------------
# In‑memory data store (for demo purposes)
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer",
                     department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager",
                     department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent problem‑solving skills.", bonus=5000),
    "E002": Performance(employee_id="E002", rating=3.8,
                        feedback="Good leadership, but needs more data analysis.",
                        bonus=3000),
}

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------

PLACEHOLDER_REGEX = re.compile(r"{([^}]+)}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in PLACEHOLDER_REGEX.finditer(template)}


def _get_attribute_value(obj, attr_path: str):
    """Retrieve nested attribute value from an object given a dot‑separated path."""
    parts = attr_path.split('.')
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise AttributeError(f"Attribute '{part}' not found in object of type {type(current).__name__}")
        current = getattr(current, part)
    return current


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the given employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders such as `{staff.name}` or `{evaluation.rating}`.

    Returns
    -------
    str
        The formatted performance summary string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template tries to access sensitive fields
        such as `feedback` or `bonus`.
    AttributeError
        If a placeholder refers to an unknown attribute path.
    """
    # Validate employee existence
    if employee_id not in EMPLOYEES:
        raise ValueError(f"Invalid employee ID: {employee_id}")

    employee = EMPLOYEES[employee_id]
    performance = PERFORMANCES.get(employee_id)

    if not performance:
        raise ValueError(f"No performance data found for employee ID: {employee_id}")

    # Detect placeholders
    placeholders = _extract_placeholders(template)

    # Define allowed paths
    allowed_paths = {
        "staff.id",
        "staff.name",
        "staff.position",
        "staff.department",
        "evaluation.rating",
    }

    # Sensitive fields that must not be exposed
    sensitive_paths = {"performance.feedback", "performance.bonus"}

    # Check for unauthorized access
    for ph in placeholders:
        if ph in sensitive_paths:
            raise ValueError(f"Unauthorized access to sensitive field: {ph}")
        if ph not in allowed_paths:
            raise AttributeError(f"Unknown placeholder: {ph}")

    # Prepare mapping for replacement
    context = {
        "staff": employee,
        "evaluation": performance,
    }

    # Function to replace placeholders
    def replacer(match):
        path = match.group(1).strip()
        obj, attr_path = context[path.split('.')[0]], '.'.join(path.split('.')[1:])
        return str(_get_attribute_value(obj, attr_path))

    # Perform substitution
    result = PLACEHOLDER_REGEX.sub(replacer, template)
    return result


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Report for {staff.name} ({staff.position})\n"
        "Department: {staff.department}\n"
        "Rating: {evaluation.rating}/5\n"
    )
    print(build_employee_report("E001", tmpl))