import re
from dataclasses import dataclass

# --------------------------------------------------------------------------- #
#  Domain model (simplified for the purpose of this exercise)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee."""
    code: str          # unique identifier
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents a performance record for an employee."""
    emp_code: str      # FK to Employee.code
    rating: float     # e.g. 4.5 out of 5
    feedback: str     # sensitive information
    bonus: float      # sensitive information


# --------------------------------------------------------------------------- #
#  In‑memory repository (replace with real persistence in production)
# --------------------------------------------------------------------------- #

_EMPLOYEES = {
    "E001": Employee(code="E001", name="Alice Smith", position="Senior Engineer",
                     department="R&D"),
    "E002": Employee(code="E002", name="Bob Jones", position="Project Manager",
                     department="Operations"),
}

_PERFORMANCES = {
    "E001": Performance(emp_code="E001", rating=4.8,
                        feedback="Excellent leadership and problem‑solving.",
                        bonus=12000.0),
    "E002": Performance(emp_code="E002", rating=4.2,
                        feedback="Good coordination, needs improvement in stakeholder communication.",
                        bonus=8000.0),
}

def _get_employee(emp_code: str) -> Employee:
    try:
        return _EMPLOYEES[emp_code]
    except KeyError as exc:
        raise ValueError(f"Employee with code '{emp_code}' not found.") from exc

def _get_performance(emp_code: str) -> Performance:
    try:
        return _PERFORMANCES[emp_code]
    except KeyError as exc:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.") from exc


# --------------------------------------------------------------------------- #
#  Report generation
# --------------------------------------------------------------------------- #

_ALLOWED_PLACEHOLDERS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

_RESTRICTED_PLACEHOLDERS = {
    "performance.feedback",
    "performance.bonus",
}

_placeholder_pattern = re.compile(r"\{([^\{\}]+)\}")

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report for the specified employee.

    Parameters
    ----------
    emp_code : str
        The unique identifier of the employee.
    summary_template : str
        A template string containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the template contains an invalid or restricted placeholder,
        or if the employee/performance data cannot be retrieved.
    """
    # Retrieve domain objects
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Find all placeholders in the template
    placeholders = set(_placeholder_pattern.findall(summary_template))

    # Validate placeholders
    for ph in placeholders:
        if ph in _RESTRICTED_PLACEHOLDERs:
            raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Invalid placeholder '{ph}' in template.")

    # Build a mapping of allowed values
    context = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": f"{performance.rating:.1f}",
    }

    # Perform substitution safely
    def _replace(match):
        key = match.group(1)
        return context[key]

    result = _placeholder_pattern.sub(_replace, summary_template)

    return result


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = ("Employee: {employee.name}\n"
            "Position: {employee.position}\n"
            "Department: {employee.department}\n"
            "Rating: {performance.rating}/5")
    print(create_performance_report("E001", tmpl))