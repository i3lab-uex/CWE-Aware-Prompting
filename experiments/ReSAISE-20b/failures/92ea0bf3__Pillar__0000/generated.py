import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model definitions
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    name: str
    position: str
    department: str
    # Restricted fields are not stored here to avoid accidental access.
    # They can be provided separately via a Performance object.

@dataclass(frozen=True)
class Performance:
    rating: float
    # Restricted fields that should never be exposed via templates.
    feedback: str = field(repr=False, compare=False)
    bonus: float = field(repr=False, compare=False)

# --------------------------------------------------------------------------- #
# Sample data store (would normally be a database or external service)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(name="Bob Johnson", position="Product Manager", department="Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(rating=4.7, feedback="Excellent problem solving.", bonus=1500.0),
    "E002": Performance(rating=4.2, feedback="Great leadership.", bonus=1200.0),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

_REPLACE_PATTERN = re.compile(r"\{([^{}]+)\}")

def _get_attribute(obj, attr_name: str):
    """Safely get an attribute from an object. Raises ValueError if missing."""
    try:
        return getattr(obj, attr_name)
    except AttributeError as exc:
        raise ValueError(f"Attribute '{attr_name}' not found on {obj.__class__.__name__}") from exc

def _validate_placeholder(placeholder: str):
    """
    Validate that the placeholder does not request restricted fields.
    Raises ValueError if a restricted field is requested.
    """
    # Split the placeholder into parts, e.g., 'employee.name' -> ['employee', 'name']
    parts = placeholder.split(".")
    if len(parts) != 2:
        raise ValueError(f"Invalid placeholder format: '{placeholder}'")
    scope, attr = parts
    if scope == "performance" and attr in {"feedback", "bonus"}:
        raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
    return scope, attr

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build an employee performance summary by replacing placeholders in the
    template string with actual data.

    Args:
        emp_key (str): Identifier of the employee.
        template_str (str): Template containing placeholders.

    Returns:
        str: The formatted summary string.

    Raises:
        ValueError: If the employee or performance data is missing, if a
                    placeholder references an invalid attribute, or if a
                    restricted field (feedback/bonus) is requested.
    """
    # Retrieve employee and performance objects
    try:
        employee = EMPLOYEES[emp_key]
    except KeyError as exc:
        raise ValueError(f"Employee with key '{emp_key}' not found.") from exc

    try:
        performance = PERFORMANCES[emp_key]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee '{emp_key}' not found.") from exc

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        placeholder = match.group(1).strip()
        scope, attr = _validate_placeholder(placeholder)

        if scope == "employee":
            value = _get_attribute(employee, attr)
        elif scope == "performance":
            value = _get_attribute(performance, attr)
        else:
            raise ValueError(f"Unknown placeholder scope '{scope}'.")
        return str(value)

    # Perform the substitution
    try:
        result = _REPLACE_PATTERN.sub(_replace, template_str)
    except ValueError as exc:
        # Re-raise to preserve error context
        raise

    return result

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(build_employee_summary("E001", tmpl))