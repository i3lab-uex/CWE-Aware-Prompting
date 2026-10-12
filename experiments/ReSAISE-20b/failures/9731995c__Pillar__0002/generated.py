import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model (simplified for this example)
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
    feedback: str = field(repr=False)   # sensitive
    bonus: float = field(repr=False)     # sensitive

# ----------------------------------------------------------------------
# In‑memory "database" (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.2, feedback="Excellent teamwork.", bonus=1500.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Strong leadership.", bonus=1200.0),
}

# ----------------------------------------------------------------------
# Helper: Safely resolve placeholder values
# ----------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{(?P<path>[a-zA-Z0-9_.]+)\}")

def _resolve_placeholder(path: str, employee: Employee, performance: Performance) -> str:
    """
    Resolve a dotted path like 'employee.name' or 'performance.rating'.
    Raises ValueError if the attribute is sensitive (feedback, bonus).
    """
    parts = path.split(".")
    if len(parts) != 2:
        raise ValueError(f"Unsupported placeholder '{path}'. Only 'employee' and 'performance' scopes are allowed.")

    scope, attr = parts
    if scope == "employee":
        obj = employee
    elif scope == "performance":
        # Prevent access to sensitive attributes
        if attr in ("feedback", "bonus"):
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
        obj = performance
    else:
        raise ValueError(f"Unknown scope '{scope}' in placeholder.")

    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' does not exist in {scope}.")
    return str(getattr(obj, attr))

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for the specified employee based on the given template.

    Parameters
    ----------
    employee_id : str
        The ID of the employee to summarize.
    template : str
        Template string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The rendered summary string.

    Raises
    ------
    ValueError
        If the employee or performance record cannot be found,
        if a placeholder references sensitive data, or if any other
        resolution error occurs.
    """
    # Retrieve employee and performance records
    employee = EMPLOYEES.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")

    performance = PERFORMANCES.get(employee_id)
    if performance is None:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")

    # Replace placeholders safely
    def repl(match: re.Match) -> str:
        path = match.group("path")
        return _resolve_placeholder(path, employee, performance)

    try:
        result = _PLACEHOLDER_RE.sub(repl, template)
    except ValueError as exc:
        # Re‑raise to signal caller
        raise

    return result

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = ("Employee {employee.name} ({employee.position}) in "
            "{employee.department} received a rating of {performance.rating}.")
    print(generate_employee_summary("E001", tmpl))