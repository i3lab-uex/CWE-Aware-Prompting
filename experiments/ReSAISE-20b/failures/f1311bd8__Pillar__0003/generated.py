import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
#   Data model (simplified for the exercise)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee."""
    emp_id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    """Represents a performance record for an employee."""
    emp_id: str
    rating: float
    # feedback and bonus are considered restricted fields

# --------------------------------------------------------------------------- #
#   In‑memory data store (would normally be a database)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Jones", position="Manager",
                     department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5),
    "E002": Performance(emp_id="E002", rating=3.8),
}

# --------------------------------------------------------------------------- #
#   Helper utilities
# --------------------------------------------------------------------------- #

# Allowed placeholders – any other will raise an exception
ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

# Regular expression to find placeholders in the template
PLACEHOLDER_RE = re.compile(r"{\s*([^}]+)\s*}")

def _get_placeholder_value(field: str, employee: Employee,
                           performance: Performance) -> str:
    """Return the string value for a given placeholder."""
    if field == "employee.name":
        return employee.name
    if field == "employee.position":
        return employee.position
    if field == "employee.department":
        return employee.department
    if field == "performance.rating":
        # Represent rating with one decimal place
        return f"{performance.rating:.1f}"
    # Should never reach here because of earlier validation
    raise ValueError(f"Unhandled placeholder: {field}")

# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, or if the template contains a
        restricted or unsupported placeholder.
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve the employee and performance records
    # --------------------------------------------------------------------- #
    employee = EMPLOYEES.get(emp_id)
    if not employee:
        raise ValueError(f"Unknown employee ID: {emp_id}")

    performance = PERFORMANCES.get(emp_id)
    if not performance:
        raise ValueError(f"No performance record for employee ID: {emp_id}")

    # --------------------------------------------------------------------- #
    # 2. Validate and substitute placeholders
    # --------------------------------------------------------------------- #
    def replace(match: re.Match) -> str:
        field = match.group(1).strip()
        if field not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Restricted or unknown placeholder: '{field}'")
        return _get_placeholder_value(field, employee, performance)

    try:
        result = PLACEHOLDER_RE.sub(replace, template_str)
    except ValueError as exc:
        # Propagate the error to the caller
        raise

    return result

# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     tmpl = (
#         "Employee Report\n"
#         "Name: {employee.name}\n"
#         "Position: {employee.position}\n"
#         "Department: {employee.department}\n"
#         "Performance Rating: {performance.rating}\n"
#     )
#     print(create_employee_report("E001", tmpl))