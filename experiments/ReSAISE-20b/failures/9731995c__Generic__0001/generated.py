import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would be ORM models or
# database records).  They are intentionally simple to keep the example
# focused on the templating logic.
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
    rating: float          # e.g. 4.5 out of 5
    feedback: str          # sensitive
    bonus: float           # sensitive


# ----------------------------------------------------------------------
# In‑memory data store (replace with database access in production).
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer",
                     department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager",
                     department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.7,
                        feedback="Excellent problem solving and teamwork.",
                        bonus=1200.00),
    "E002": Performance(employee_id="E002", rating=4.2,
                        feedback="Strong leadership, but needs to improve delegation.",
                        bonus=900.00),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _fetch_employee(employee_id: str) -> Employee:
    """Retrieve an employee record by ID."""
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' not found.") from exc


def _fetch_performance(employee_id: str) -> Performance:
    """Retrieve a performance record by employee ID."""
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.") from exc


def _replace_placeholders(template: str, context: Dict[str, Any]) -> str:
    """
    Replace placeholders in the form {key} with values from context.
    Raises ValueError if a placeholder refers to a disallowed field.
    """
    # Allowed keys: employee.* and performance.rating
    allowed_keys = {"employee.name", "employee.position",
                    "employee.department", "performance.rating"}

    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in allowed_keys:
            raise ValueError(f"Access to sensitive or unknown field '{key}' is not permitted.")
        return str(context[key])

    pattern = re.compile(r"\{([^}]+)\}")
    return pattern.sub(repl, template)


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The ID of the employee to generate a summary for.
    template : str
        A string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The generated summary string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee or performance record does not exist, if a placeholder
        references a disallowed field (e.g., feedback or bonus), or any other
        error occurs during processing.
    """
    # Fetch data
    employee = _fetch_employee(employee_id)
    performance = _fetch_performance(employee_id)

    # Build context dictionary for placeholder replacement
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Replace placeholders safely
    return _replace_placeholders(template, context)


# ----------------------------------------------------------------------
# Example usage (commented out; remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee {employee.name} ({employee.position}) in "
        "{employee.department} received a rating of {performance.rating}."
    )
    print(generate_employee_summary("E001", tmpl))