import re
from typing import Dict

# Assume these classes are defined elsewhere in the project.
# They provide read‑only attributes for security reasons.
class Employee:
    def __init__(self, emp_id: str, name: str, position: str):
        self.id = emp_id
        self.name = name
        self.position = position

class Performance:
    def __init__(self, rating: str):
        self.rating = rating


# Dummy data store for demonstration purposes.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Developer"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("Excellent"),
    "E002": Performance("Good"),
}


# Mapping of allowed placeholders to the corresponding attribute paths.
_ALLOWED_PLACEHOLDERS = {
    "staff.name": lambda emp: emp.name,
    "staff.position": lambda emp: emp.position,
    "evaluation.rating": lambda perf: perf.rating,
}

# Placeholders that are forbidden to expose (e.g., sensitive data).
_FORBIDDEN_PLACEHOLDERS = {"feedback", "bonus"}


def _validate_placeholders(template: str) -> None:
    """
    Ensure the template does not contain any forbidden placeholders.
    Raises ValueError if it does.
    """
    for placeholder in _FORBIDDEN_PLACEHOLDERS:
        if f"{{{placeholder}}}" in template or f"{{{placeholder}.": in template:
            raise ValueError(f"Unauthorized placeholder '{placeholder}' accessed.")


def _get_employee_and_performance(employee_id: str):
    """
    Retrieve the Employee and Performance objects for the given ID.
    Raises ValueError if the employee_id is unknown.
    """
    emp = EMPLOYEES.get(employee_id)
    perf = PERFORMANCES.get(employee_id)

    if not emp or not perf:
        raise ValueError(f"Employee ID '{employee_id}' is invalid.")

    return emp, perf


def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the specified employee using the provided
    template string.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        Template string containing placeholders like '{staff.name}',
        '{staff.position}', and '{evaluation.rating}'.

    Returns
    -------
    str
        The formatted performance report string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template contains
        disallowed placeholders.
    """
    # 1. Validate that no forbidden data is requested.
    _validate_placeholders(template)

    # 2. Retrieve employee and performance data.
    emp, perf = _get_employee_and_performance(employee_id)

    # 3. Replace placeholders.
    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unknown placeholder '{{{key}}}'.")
        # Decide whether to fetch from employee or performance.
        value_func = _ALLOWED_PLACEHOLDERS[key]
        # The function knows whether it needs emp or perf.
        return str(value_func(emp if "staff" in key else perf))

    pattern = re.compile(r"\{([^\}]+)\}")
    result = pattern.sub(replace, template)

    return result