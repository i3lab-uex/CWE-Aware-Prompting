import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked data structures – in a real system these would be imported
# from the company's data layer.
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    emp_id: str
    name: str
    position: str
    department: str

@dataclass(frozen=True)
class Performance:
    emp_id: str
    rating: float
    feedback: str  # restricted
    bonus: float   # restricted

# ----------------------------------------------------------------------
# In‑memory "database" – replace with real persistence in production.
# ----------------------------------------------------------------------
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Engineer",
                     department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Jones", position="Manager",
                     department="Sales"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5,
                        feedback="Excellent problem solving.",
                        bonus=1500.0),
    "E002": Performance(emp_id="E002", rating=3.8,
                        feedback="Strong leadership.",
                        bonus=1200.0),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return _EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Unknown employee ID: {emp_id}") from exc

def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance record by ID, raising ValueError if not found."""
    try:
        return _PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"No performance data for employee ID: {emp_id}") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee using the provided
    template string.

    The template may contain placeholders in the form {employee.field} or
    {performance.field}. Restricted fields (feedback, bonus) are not allowed.
    Any attempt to reference them will raise a ValueError.

    Parameters
    ----------
    emp_id : str
        The unique employee identifier.
    summary_template : str
        A template string containing placeholders.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if restricted fields are referenced,
        or if an unknown placeholder field is used.
    """
    # Validate employee ID and retrieve data
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Allowed fields for each namespace
    allowed_employee_fields = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
    }
    allowed_performance_fields = {
        "rating": performance.rating,
    }

    # Build a combined namespace for formatting
    namespace: Dict[str, Any] = {
        "employee": allowed_employee_fields,
        "performance": allowed_performance_fields,
    }

    # Regular expression to find all placeholders
    placeholder_pattern = re.compile(r"{\s*(?P<ns>\w+)\.(?P<field>\w+)\s*}")

    # Check for restricted fields before formatting
    for match in placeholder_pattern.finditer(summary_template):
        ns = match.group("ns")
        field = match.group("field")

        if ns == "performance" and field in {"feedback", "bonus"}:
            raise ValueError(f"Access to restricted performance field '{field}' is not allowed.")

        if ns == "employee":
            if field not in allowed_employee_fields:
                raise ValueError(f"Unknown employee field '{field}'.")
        elif ns == "performance":
            if field not in allowed_performance_fields:
                raise ValueError(f"Unknown performance field '{field}'.")
        else:
            raise ValueError(f"Unknown namespace '{ns}' in placeholder.")

    # Perform safe formatting by replacing placeholders manually
    def replacement(match: re.Match) -> str:
        ns, field = match.group("ns"), match.group("field")
        return str(namespace[ns][field])

    formatted = placeholder_pattern.sub(replacement, summary_template)
    return formatted

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = (
#         "Employee {employee.name} ({employee.position}) in "
#         "{employee.department} achieved a rating of {performance.rating}. "
#     )
#     print(create_performance_summary("E001", tmpl))