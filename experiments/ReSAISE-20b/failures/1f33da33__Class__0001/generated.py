import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked domain classes (replace with real implementations in production)
# ----------------------------------------------------------------------
@dataclass
class Performance:
    rating: float
    feedback: str  # Sensitive, should not be exposed
    bonus: float   # Sensitive, should not be exposed

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    performance: Performance

# ----------------------------------------------------------------------
# In‑memory "database" of employees for demonstration purposes
# ----------------------------------------------------------------------
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="Research & Development",
        performance=Performance(
            rating=4.7,
            feedback="Excellent leadership and problem solving.",
            bonus=12000
        )
    ),
    # Add more employees as needed...
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee_by_id(emp_id: str) -> Employee:
    """Retrieve an employee from the database by ID."""
    emp = EMPLOYEE_DB.get(emp_id)
    if not emp:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    return emp

def _extract_placeholders(template: str) -> set:
    """Return a set of unique placeholder names found in the template."""
    return set(re.findall(r"{([^}]+)}", template))

def _validate_and_resolve_placeholders(placeholders: set, emp: Employee) -> Dict[str, Any]:
    """
    Resolve allowed placeholders to their actual values.
    Raises ValueError if a placeholder is disallowed or unknown.
    """
    # Define the mapping of allowed placeholders to attribute access paths
    allowed_map = {
        "employee.name": lambda e: e.name,
        "employee.position": lambda e: e.position,
        "employee.department": lambda e: e.department,
        "performance.rating": lambda e: e.performance.rating,
    }

    resolved = {}
    for ph in placeholders:
        if ph not in allowed_map:
            raise ValueError(f"Disallowed or unknown placeholder: '{ph}'.")
        resolved[ph] = allowed_map[ph](emp)
    return resolved

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using the supplied template.

    Args:
        emp_id (str): Unique identifier for an employee.
        summary_template (str): Template string containing placeholders such as
                                '{employee.name}', '{performance.rating}', etc.

    Returns:
        str: Formatted performance summary string.

    Raises:
        ValueError: If the employee ID is invalid or if the template contains
                    disallowed placeholders (e.g., '{performance.feedback}' or
                    '{performance.bonus}').
    """
    # Retrieve employee data (will raise ValueError if not found)
    emp = _get_employee_by_id(emp_id)

    # Extract placeholders from the template
    placeholders = _extract_placeholders(summary_template)

    # Resolve placeholder values, validating access control
    resolved_values = _validate_and_resolve_placeholders(placeholders, emp)

    # Perform the actual formatting
    try:
        formatted = summary_template.format(**resolved_values)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return formatted