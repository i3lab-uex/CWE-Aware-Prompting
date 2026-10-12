import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data models (in a real system these would be imported from the
# company's database layer)
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
    bonus: int     # Sensitive

# ----------------------------------------------------------------------
# In‑memory data store (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Manager",
                     department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent leadership and technical skills.",
                        bonus=5000),
    "E002": Performance(employee_id="E002", rating=3.8,
                        feedback="Strong sales growth, needs improvement in team communication.",
                        bonus=3000),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(employee_id: str) -> Employee:
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee with id {employee_id!r} not found") from exc

def _get_performance(employee_id: str) -> Performance:
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee id {employee_id!r} not found") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as `{employee.name}` or
        `{performance.rating}`.

    Returns
    -------
    str
        The template with placeholders replaced by actual values.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if a
        placeholder that exposes sensitive information is used.
    """
    # Retrieve data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Define allowed placeholders
    allowed_placeholders = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating",
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    found_placeholders = set(placeholder_pattern.findall(template))

    # Check for disallowed placeholders
    if not found_placeholders.issubset(allowed_placeholders):
        disallowed = found_placeholders - allowed_placeholders
        raise ValueError(f"Template contains disallowed placeholders: {', '.join(disallowed)}")

    # Build a mapping for replacement
    replace_map = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": f"{performance.rating:.1f}",
    }

    # Perform the replacement
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return replace_map[key]

    result = placeholder_pattern.sub(_replace, template)
    return result

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee {employee.name} ({employee.position}) in "
        "{employee.department} department has a performance rating of "
        "{performance.rating}."
    )
    print(generate_employee_summary("E001", tmpl))