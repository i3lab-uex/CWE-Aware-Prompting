import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Data models (minimal implementation for demonstration)
# ------------------------------------------------------------------
@dataclass
class Performance:
    rating: str
    # Sensitive fields – should never be exposed via the template
    feedback: str = field(repr=False, default="")
    bonus: float = field(repr=False, default=0.0)

@dataclass
class Employee:
    key: str
    name: str
    position: str
    department: str
    performance: Performance

# ------------------------------------------------------------------
# In‑memory "database" of employees (replace with real persistence)
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {}

def register_employee(emp: Employee) -> None:
    """Utility to add an employee to the in‑memory store."""
    EMPLOYEES[emp.key] = emp

def get_employee(emp_key: str) -> Employee:
    """Retrieve an employee by key, raising ValueError if not found."""
    try:
        return EMPLOYEES[emp_key]
    except KeyError as exc:
        raise ValueError(f"Employee with key '{emp_key}' not found") from exc

# ------------------------------------------------------------------
# Template rendering logic
# ------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating"
}

# Regular expression to find placeholders like {employee.name}
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

def _resolve_placeholder(obj: object, attr_path: str):
    """
    Resolve an attribute path (e.g. 'employee.name') on the given object.
    Raises ValueError if the attribute does not exist or is disallowed.
    """
    if attr_path not in _ALLOWED_PLACEHOLDERS:
        raise ValueError(f"Access to placeholder '{attr_path}' is not allowed")

    parts = attr_path.split(".")
    current_obj = obj
    for part in parts:
        if not hasattr(current_obj, part):
            raise ValueError(f"Attribute '{part}' does not exist on object of type {type(current_obj).__name__}")
        current_obj = getattr(current_obj, part)
    return str(current_obj)

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Render an employee performance summary based on the supplied template.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee does not exist, if a placeholder refers to an
        unsupported or restricted field, or if the template contains an
        invalid placeholder.
    """
    # Retrieve employee data
    emp = get_employee(emp_key)

    def replacement(match: re.Match) -> str:
        placeholder = match.group(1)
        # Resolve the value for this placeholder
        return _resolve_placeholder(emp, placeholder)

    try:
        # Perform safe substitution; only allowed placeholders are processed
        result = _PLACEHOLDER_RE.sub(replacement, template_str)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to build summary: {exc}") from exc

    return result


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Register a sample employee
    emp = Employee(
        key="E123",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Great team player and innovator.",
            bonus=1500.00
        )
    )
    register_employee(emp)

    # Define a template
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )

    # Build summary
    print(build_employee_summary("E123", tmpl))