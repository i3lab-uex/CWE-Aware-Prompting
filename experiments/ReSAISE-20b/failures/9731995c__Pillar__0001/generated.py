import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Domain model
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Employee:
    """Represents an employee record."""
    id: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    """Represents a performance review record."""
    employee_id: str
    rating: float
    feedback: str = field(repr=False)  # sensitive data
    bonus: float = field(default=0.0, repr=False)  # sensitive data


# ------------------------------------------------------------------
# In‑memory storage (simulating a database)
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {}
PERFORMANCES: Dict[str, Performance] = {}


# ------------------------------------------------------------------
# Utility
# ------------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _get_attribute(obj, attr: str):
    """Return the attribute value or raise ValueError."""
    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' does not exist.")
    return getattr(obj, attr)


def _validate_placeholder(placeholder: str):
    """
    Ensure the placeholder does not reference sensitive data.
    Raises ValueError if it does or if syntax is invalid.
    """
    parts = placeholder.split(".")
    if len(parts) != 2:
        raise ValueError(f"Invalid placeholder syntax: '{{{placeholder}}}'")

    obj_name, attr = parts
    if obj_name not in ("employee", "performance"):
        raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{placeholder}}}'")

    if obj_name == "performance" and attr in ("feedback", "bonus"):
        raise ValueError(f"Access to sensitive field '{attr}' is prohibited.")


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The rendered summary string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee or performance record is missing, if a placeholder
        references non‑existent data, or if it attempts to access sensitive
        fields.
    """
    # Fetch the required records (simulate database access)
    employee = EMPLOYEES.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")

    performance = PERFORMANCES.get(employee_id)
    if performance is None:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")

    # Replace placeholders
    def replacement(match: re.Match) -> str:
        placeholder = match.group(1)
        _validate_placeholder(placeholder)

        obj_name, attr = placeholder.split(".")
        if obj_name == "employee":
            value = _get_attribute(employee, attr)
        else:  # obj_name == "performance"
            value = _get_attribute(performance, attr)

        return str(value)

    try:
        result = PLACEHOLDER_RE.sub(replacement, template)
    except re.error as exc:
        raise ValueError(f"Invalid regex operation: {exc}") from exc

    return result


# ------------------------------------------------------------------
# Example usage (for illustration only; remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Populate the in‑memory storage
    EMPLOYEES["E001"] = Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D")
    PERFORMANCES["E001"] = Performance(employee_id="E001", rating=4.5,
                                        feedback="Excellent work on the project.",
                                        bonus=1500.0)

    tmpl = ("Employee: {employee.name}\n"
            "Position: {employee.position}\n"
            "Department: {employee.department}\n"
            "Rating: {performance.rating}")

    print(generate_employee_summary("E001", tmpl))