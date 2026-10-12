import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Mocked data models (in a real system these would be imported from
# the company's existing modules)
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Performance:
    rating: float
    feedback: str   # restricted
    bonus: float    # restricted

@dataclass(frozen=True)
class Employee:
    emp_id: str
    name: str
    position: str
    department: str
    performance: Performance

# --------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# --------------------------------------------------------------------

EMPLOYEE_DB: Dict[str, Employee] = {}

def _load_demo_data() -> None:
    """Populate the mock database with sample employees."""
    global EMPLOYEE_DB
    EMPLOYEE_DB = {
        "E001": Employee(
            emp_id="E001",
            name="Alice Johnson",
            position="Senior Engineer",
            department="R&D",
            performance=Performance(rating=4.5, feedback="Excellent problem solving", bonus=1500.0),
        ),
        "E002": Employee(
            emp_id="E002",
            name="Bob Smith",
            position="Project Manager",
            department="Operations",
            performance=Performance(rating=4.0, feedback="Strong leadership", bonus=1200.0),
        ),
    }

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

_REPLACE_PATTERN = re.compile(r"\{(?P<path>[^{}]+)\}")

# Fields that are disallowed in the template
_RESTRICTED_FIELDS = {"feedback", "bonus"}

def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Return a formatted performance summary for the given employee.

    Args:
        emp_id: The unique identifier of the employee.
        summary_template: A string containing placeholders such as
            '{employee.name}', '{performance.rating}', etc.

    Returns:
        A string with all placeholders replaced by the employee's data.

    Raises:
        ValueError: If an invalid employee ID is supplied or if the
            template attempts to access restricted fields.
    """
    # --------------------------------------------------------------------
    # 1. Validate employee ID
    # --------------------------------------------------------------------
    if emp_id not in EMPLOYEE_DB:
        raise ValueError(f"Unknown employee ID: {emp_id}")

    employee = EMPLOYEE_DB[emp_id]

    # --------------------------------------------------------------------
    # 2. Resolve placeholders
    # --------------------------------------------------------------------
    def _resolve(match: re.Match) -> str:
        path = match.group("path").strip()
        # Expect format: <object>.<attribute>
        if "." not in path:
            raise ValueError(f"Invalid placeholder syntax: '{{{path}}}'")
        obj_name, attr = path.split(".", 1)

        # Map object names to actual objects
        if obj_name == "employee":
            base_obj = employee
        elif obj_name == "performance":
            base_obj = employee.performance
        else:
            raise ValueError(f"Unknown placeholder object: '{obj_name}'")

        # Check for restricted fields
        if obj_name == "performance" and attr in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed")

        # Retrieve attribute value
        if not hasattr(base_obj, attr):
            raise ValueError(f"Attribute '{attr}' does not exist on '{obj_name}'")
        value = getattr(base_obj, attr)

        # Convert to string for insertion
        return str(value)

    try:
        result = _REPLACE_PATTERN.sub(_resolve, summary_template)
    except re.error as exc:
        raise ValueError(f"Template parsing error: {exc}") from exc

    return result


# --------------------------------------------------------------------
# Example usage (for demonstration; remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    _load_demo_data()

    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )

    try:
        summary = create_performance_summary("E001", template)
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")