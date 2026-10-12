import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Dummy data structures for the sake of a self‑contained example
# In a real system these would be replaced by ORM models or API calls.
# --------------------------------------------------------------------
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
    feedback: str = field(repr=False)  # Sensitive
    bonus: float = field(repr=False)   # Sensitive

# --------------------------------------------------------------------
# Sample in‑memory store
# --------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(id="E002", name="Bob Jones", position="Product Manager",
                     department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent leadership and coding skills.",
                        bonus=1500.00),
    "E002": Performance(employee_id="E002", rating=3.8,
                        feedback="Strong product vision but needs better time management.",
                        bonus=1200.00),
}

# --------------------------------------------------------------------
# Helper: safe placeholder extraction
# --------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str):
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in PLACEHOLDER_RE.finditer(template)}

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee key is unknown, or if a restricted field is requested.
    """
    # Retrieve data
    employee = EMPLOYEES.get(emp_key)
    if not employee:
        raise ValueError(f"Unknown employee key: {emp_key}")

    performance = PERFORMANCES.get(emp_key)
    if not performance:
        raise ValueError(f"No performance data for employee key: {emp_key}")

    # Define allowed fields
    allowed_fields = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating",
    }

    # Inspect placeholders
    placeholders = _extract_placeholders(template_str)
    for ph in placeholders:
        if ph not in allowed_fields:
            raise ValueError(f"Access to restricted or unknown field '{ph}' is not permitted")

    # Build context dictionary for formatting
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Perform safe formatting
    try:
        formatted = template_str.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Formatting error: {exc}") from exc

    return formatted


# --------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} ({employee.department})\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(build_employee_summary("E001", tmpl))