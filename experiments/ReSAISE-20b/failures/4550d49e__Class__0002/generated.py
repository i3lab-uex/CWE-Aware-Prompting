import re
from typing import Dict

# Assume these classes are defined elsewhere in the codebase.
# They should expose only public attributes for security reasons.
class Employee:
    def __init__(self, employee_id: str, name: str, position: str,
                 department: str, performance):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance

class Performance:
    def __init__(self, rating: str, feedback: str, bonus: float):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# Dummy data store – in a real system this would query a database.
EMPLOYEE_DB: Dict[str, Employee] = {}

def _get_employee_by_id(employee_id: str) -> Employee:
    """
    Retrieve an employee instance by ID. Raises KeyError if not found.
    """
    try:
        return EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{employee_id}' not found.") from exc

def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholder names (e.g., 'employee.name') from the template.
    """
    # Pattern matches {some.text} but ignores escaped braces {{ or }}
    pattern = r"\{([^\{\}]*)\}"
    return set(re.findall(pattern, template))

def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Construct a performance summary for the specified employee.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    report_template : str
        A template string containing placeholders such as
        '{employee.name}', '{performance.rating}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template attempts to
        access restricted fields like 'feedback' or 'bonus'.
    """
    # 1. Retrieve employee data
    employee = _get_employee_by_id(employee_id)

    # 2. Define allowed placeholder mappings
    mapping: Dict[str, str] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": employee.performance.rating,
    }

    # 3. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    for ph in placeholders:
        if ph not in mapping:
            # Disallow sensitive fields
            restricted = {"performance.feedback", "performance.bonus"}
            if ph in restricted:
                raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
            # Unknown placeholder
            raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # 4. Perform safe formatting
    try:
        formatted_report = report_template.format(**mapping)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted_report