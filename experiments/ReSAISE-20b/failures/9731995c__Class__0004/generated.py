import re
from typing import Dict, Any

# Dummy data store – in a real system this would query a database
EMPLOYEE_DB: Dict[str, Any] = {
    "E001": {"name": "Alice Smith", "position": "Senior Engineer", "department": "R&D"},
    "E002": {"name": "Bob Johnson", "position": "Project Manager", "department": "Operations"},
}

PERFORMANCE_DB: Dict[str, Any] = {
    "E001": {"rating": 4.5, "feedback": "Excellent problem‑solving skills.", "bonus": "$5,000"},
    "E002": {"rating": 3.8, "feedback": "Good leadership.", "bonus": "$2,000"},
}


def _get_employee_by_id(employee_id: str) -> Dict[str, Any]:
    """
    Retrieve employee data from the database.
    Raises ValueError if the employee does not exist.
    """
    employee = EMPLOYEE_DB.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")
    return employee


def _get_performance_by_id(employee_id: str) -> Dict[str, Any]:
    """
    Retrieve performance data from the database.
    Raises ValueError if the performance record does not exist.
    """
    perf = PERFORMANCE_DB.get(employee_id)
    if perf is None:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")
    return perf


def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee by replacing placeholders in the
    provided template with actual data.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Sensitive fields like feedback or bonus are
        prohibited.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee or performance record cannot be found, or if the
        template attempts to access sensitive data (feedback or bonus).
    """
    # Validate placeholders for sensitive fields
    if re.search(r"\{performance\.feedback\}", template, flags=re.IGNORECASE):
        raise ValueError("Access to sensitive performance feedback is not allowed.")
    if re.search(r"\{performance\.bonus\}", template, flags=re.IGNORECASE):
        raise ValueError("Access to sensitive performance bonus is not allowed.")

    # Retrieve data
    employee = _get_employee_by_id(employee_id)
    performance = _get_performance_by_id(employee_id)

    # Build a combined namespace for substitution
    namespace = {
        "employee": employee,
        "performance": performance,
    }

    # Custom formatter that safely replaces placeholders
    class SafeFormatter(re.Formatter):
        def get_value(self, key, args, kwargs):
            if isinstance(key, str):
                # Support nested keys like 'employee.name'
                parts = key.split(".")
                value = namespace
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        raise ValueError(f"Invalid placeholder: {{{key}}}")
                return value
            return super().get_value(key, args, kwargs)

    formatter = SafeFormatter()
    try:
        result = formatter.format(template)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Error processing template: {exc}") from exc

    return result