import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mock data structures (replace with real database access in production)
# ----------------------------------------------------------------------


@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str = field(repr=False)  # sensitive
    bonus: float = field(default=0.0, repr=False)  # sensitive


# In‑memory "database" for demonstration purposes
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on project X.", bonus=5000),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership.", bonus=3000),
}


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------


def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The ID of the employee.
    template : str
        A string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Placeholders referencing sensitive data
        (feedback or bonus) are disallowed.

    Returns
    -------
    str
        The template with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee or performance record cannot be found,
        if a placeholder refers to missing data, or
        if the template attempts to access sensitive information.
    """
    # Retrieve objects from "database"
    employee = EMPLOYEE_DB.get(employee_id)
    if not employee:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")

    performance = PERFORMANCE_DB.get(employee_id)
    if not performance:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")

    # Mapping from root names in placeholders to actual objects
    context = {
        "employee": employee,
        "performance": performance,
    }

    # Sensitive attributes that are not allowed in templates
    sensitive_attrs = {"feedback", "bonus"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    matches = placeholder_pattern.findall(template)

    for placeholder in matches:
        # Split into root and attribute chain, e.g., 'employee.name'
        parts = placeholder.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")

        root, attr = parts
        obj = context.get(root)
        if obj is None:
            raise ValueError(f"Unknown placeholder root: '{root}' in '{{{placeholder}}}'")

        # Prevent access to sensitive attributes
        if attr.lower() in sensitive_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed.")

        # Retrieve the attribute value
        if not hasattr(obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on object '{root}'.")
        value = getattr(obj, attr)

        # Replace the placeholder with its string representation
        template = template.replace(f"{{{placeholder}}}", str(value))

    return template


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    tmpl = (
        "Employee {employee.name} ({employee.position}) in the "
        "{employee.department} department has a performance rating of "
        "{performance.rating}."
    )
    try:
        summary = generate_employee_summary("E001", tmpl)
        print(summary)
    except ValueError as exc:
        print(f"Error: {exc}")