import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Mock data structures (in a real system these would be imported)
# --------------------------------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    position: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str   # Sensitive data
    bonus: float    # Sensitive data

# --------------------------------------------------------------------
# In-memory "database" for demonstration purposes
# --------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent work on project X.", bonus=1200.0),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good leadership.", bonus=900.0),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def get_employee_by_id(employee_id: str) -> Employee:
    """Retrieve an employee object by ID."""
    emp = EMPLOYEES.get(employee_id)
    if not emp:
        raise ValueError(f"Invalid employee ID: {employee_id}")
    return emp

def get_performance_by_employee_id(employee_id: str) -> Performance:
    """Retrieve a performance object by employee ID."""
    perf = PERFORMANCES.get(employee_id)
    if not perf:
        raise ValueError(f"No performance record for employee ID: {employee_id}")
    return perf

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def compile_employee_evaluation(employee_id: str, template: str) -> str:
    """
    Generate a performance summary for the given employee by replacing
    placeholders in the template with actual data.

    Allowed placeholders:
        {personnel.name}
        {personnel.position}
        {performance.rating}

    Any attempt to access unauthorized fields (e.g., feedback, bonus)
    or an invalid employee ID will raise a ValueError.
    """
    # Retrieve data
    employee = get_employee_by_id(employee_id)
    performance = get_performance_by_employee_id(employee_id)

    # Build context dictionary
    context: Dict[str, Any] = {
        "personnel": {"name": employee.name, "position": employee.position},
        "performance": {"rating": performance.rating}
    }

    # Identify placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(template)

    # Define allowed paths
    allowed_paths = {
        "personnel.name",
        "personnel.position",
        "performance.rating"
    }

    # Validate placeholders
    for ph in placeholders:
        if ph not in allowed_paths:
            raise ValueError(f"Unauthorized placeholder or unknown field: {{{ph}}}")

    # Safe formatting using a custom mapping that returns empty string for missing keys
    class SafeDict(dict):
        def __missing__(self, key):
            return ""

    # Prepare nested mapping for format_map
    safe_context = SafeDict(
        personnel=SafeDict(name=context["personnel"]["name"],
                           position=context["personnel"]["position"]),
        performance=SafeDict(rating=str(context["performance"]["rating"]))
    )

    # Perform formatting
    try:
        result = template.format_map(safe_context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return result