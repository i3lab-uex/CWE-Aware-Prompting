import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Domain models (simplified for this example)
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
    feedback: str  # Sensitive
    bonus: float   # Sensitive


# ----------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent problem‑solving skills.", bonus=1200),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Strong leadership.", bonus=800),
}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r"\{([^}]+)\}")

_ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}


def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in _RE_PLACEHOLDER.finditer(template)}


def _build_context(emp: Employee, perf: Performance) -> dict:
    """Create a flat context dictionary for string formatting."""
    ctx = {}
    # Employee fields
    for field in ("name", "position", "department"):
        ctx[f"employee.{field}"] = getattr(emp, field)
    # Performance fields
    ctx["performance.rating"] = perf.rating
    return ctx


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted performance report for the given employee.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, or if restricted fields are requested.
    """
    # Retrieve domain objects
    employee = EMPLOYEES.get(emp_id)
    if not employee:
        raise ValueError(f"Employee with id '{emp_id}' does not exist.")
    performance = PERFORMANCES.get(emp_id)
    if not performance:
        raise ValueError(f"Performance record for employee id '{emp_id}' is missing.")

    # Inspect placeholders
    placeholders = _extract_placeholders(template_str)
    for ph in placeholders:
        if ph not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted or unknown field '{ph}' is not allowed.")

    # Build context for formatting
    ctx = _build_context(employee, performance)

    try:
        result = template_str.format(**ctx)
    except KeyError as exc:
        # This should not happen due to the earlier check, but guard anyway
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(create_employee_report("E001", template))