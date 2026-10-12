import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Mocked domain classes – in real code these would be imported from the
# application’s data layer.
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Performance:
    rating: str
    feedback: str  # Sensitive – should not be exposed via the template
    bonus: float   # Sensitive – should not be exposed via the template

@dataclass(frozen=True)
class Employee:
    id: str
    name: str
    position: str
    department: str
    performance: Performance

# --------------------------------------------------------------------
# In‑memory "database" of employees – replace with real persistence in
# production.
# --------------------------------------------------------------------

EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding contribution to the AI project.",
            bonus=5000.0,
        ),
    ),
    "E002": Employee(
        id="E002",
        name="Bob Johnson",
        position="Project Manager",
        department="Operations",
        performance=Performance(
            rating="Good",
            feedback="Managed the transition to Agile smoothly.",
            bonus=3000.0,
        ),
    ),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"{(?P<path>[^}]+)}")

def _resolve_path(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path on an object.
    Raises AttributeError if any part of the path is missing.
    """
    parts = path.split(".")
    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise AttributeError(f"Attribute '{part}' not found on {current!r}")
        current = getattr(current, part)
    return current

def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference sensitive data.
    Sensitive fields are 'feedback' and 'bonus'.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        path = match.group("path")
        if any(unsafe in path.split(".") for unsafe in ("feedback", "bonus")):
            raise ValueError(f"Unauthorized access to sensitive field '{path}' in template.")

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the given employee using the supplied
    template string.

    Parameters
    ----------
    employee_id : str
        Unique identifier for the employee.
    template : str
        Template string containing placeholders like `{staff.name}`.

    Returns
    -------
    str
        The formatted performance summary string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template references
        sensitive data such as feedback or bonus.
    """
    # Validate template for forbidden fields first
    _validate_template(template)

    # Retrieve employee data – raise ValueError if not found
    try:
        employee = EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {employee_id}") from exc

    # Prepare a namespace that mimics the expected structure in the template
    namespace: Dict[str, Any] = {
        "staff": employee,
        "performance": employee.performance,
    }

    # Perform substitution manually to avoid using str.format with
    # potential injection issues.  We replace each placeholder by its value.
    def replacer(match: re.Match) -> str:
        path = match.group("path")
        # Resolve the attribute chain starting from the namespace dict
        try:
            value = _resolve_path(namespace, path)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{path}' in template.") from exc
        return str(value)

    result = _PLACEHOLDER_RE.sub(replacer, template)
    return result

# --------------------------------------------------------------------
# Example usage (uncomment to test):
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = (
#         "Employee Report:\n"
#         "- Name: {staff.name}\n"
#         "- Position: {staff.position}\n"
#         "- Department: {staff.department}\n"
#         "- Rating: {performance.rating}"
#     )
#     print(build_employee_report("E001", tmpl))