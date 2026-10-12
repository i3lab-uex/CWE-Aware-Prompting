import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Data models (normally these would be provided by the system)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    emp_id: str
    rating: float  # e.g., out of 5.0
    feedback: str  # sensitive – must not be exposed via template
    bonus: float   # sensitive – must not be exposed via template

# --------------------------------------------------------------------------- #
# In‑memory "database" of employees and performances
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Engineer", department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Jones", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.2, feedback="Excellent problem solving.", bonus=1200.00),
    "E002": Performance(emp_id="E002", rating=3.8, feedback="Good team leadership.", bonus=800.00),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

_PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

_ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "performance.rating",
}

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of unique placeholders found in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_PATTERN.finditer(template)}

def _get_context(emp: Employee, perf: Performance) -> Dict[str, Any]:
    """Build a context dictionary mapping placeholder names to values."""
    return {
        "employee.name": emp.name,
        "employee.position": emp.position,
        "performance.rating": perf.rating,
    }

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Return a formatted employee performance report.

    Args:
        emp_id: Identifier of the employee.
        template_str: Template string containing placeholders such as
                      '{employee.name}', '{performance.rating}'.

    Returns:
        A string with placeholders replaced by actual data.

    Raises:
        ValueError: If the employee ID is unknown, a placeholder refers
                    to an unallowed or missing field, or restricted fields
                    (feedback/bonus) are requested.
    """
    # 1. Retrieve data safely
    emp = EMPLOYEES.get(emp_id)
    perf = PERFORMANCES.get(emp_id)

    if not emp or not perf:
        raise ValueError(f"Unknown employee ID: {emp_id}")

    # 2. Parse placeholders and validate
    placeholders = _extract_placeholders(template_str)

    for ph in placeholders:
        if ph not in _ALLOWED_FIELDS:
            # Detect restricted fields or typos
            if ph.startswith("employee.") or ph.startswith("performance."):
                # Any field not in the allowed set is considered restricted
                raise ValueError(f"Access to restricted or unknown field '{ph}' is not permitted.")
            else:
                raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # 3. Build context and format
    context = _get_context(emp, perf)

    try:
        formatted = template_str.format(**context)
    except KeyError as exc:
        # Should not happen due to earlier validation
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted

# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report for {employee.name}\n"
        "Position: {employee.position}\n"
        "Performance Rating: {performance.rating}/5.0\n"
    )
    print(create_employee_report("E001", tmpl))