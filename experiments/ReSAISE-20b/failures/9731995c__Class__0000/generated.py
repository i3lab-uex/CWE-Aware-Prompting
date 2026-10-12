import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked data structures (replace with real implementations in production)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, employee_id: str, name: str, position: str,
                 department: str):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee_id: str, rating: float,
                 feedback: str, bonus: float):
        self.employee_id = employee_id
        self.rating = rating
        self.feedback = feedback          # Sensitive
        self.bonus = bonus                # Sensitive

# ----------------------------------------------------------------------
# Data access layer (replace with real data source in production)
# ----------------------------------------------------------------------
def _get_employee(employee_id: str) -> Employee:
    """
    Retrieve an Employee instance by ID.
    Raises ValueError if not found.
    """
    # In a real system, replace with database or API call
    dummy_db: Dict[str, Employee] = {
        "E001": Employee("E001", "Alice Smith", "Software Engineer",
                         "Engineering"),
        "E002": Employee("E002", "Bob Johnson", "Product Manager",
                         "Product"),
    }
    employee = dummy_db.get(employee_id)
    if not employee:
        raise ValueError(f"Employee with ID '{employee_id}' not found.")
    return employee

def _get_performance(employee_id: str) -> Performance:
    """
    Retrieve a Performance instance by employee ID.
    Raises ValueError if not found.
    """
    # In a real system, replace with database or API call
    dummy_perf_db: Dict[str, Performance] = {
        "E001": Performance("E001", 4.5,
                            "Excellent contribution to core modules.",
                            12000.0),
        "E002": Performance("E002", 3.8,
                            "Strong leadership in cross‑functional teams.",
                            8000.0),
    }
    perf = dummy_perf_db.get(employee_id)
    if not perf:
        raise ValueError(f"Performance record for employee ID '{employee_id}' "
                         "not found.")
    return perf

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
_SENSITIVE_KEYS = {"feedback", "bonus"}

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Placeholders are of the form {object.attribute}.
    """
    pattern = r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return {f"{m.group(1)}.{m.group(2)}" for m in re.finditer(pattern, template)}

def _replace_placeholders(template: str,
                          context: Dict[str, Any]) -> str:
    """
    Replace placeholders in the template with values from context.
    Raises ValueError if a placeholder refers to sensitive data or is missing.
    """
    def _replacement(match: re.Match) -> str:
        obj_name, attr = match.group(1), match.group(2)
        key = f"{obj_name}.{attr}"
        if key in _SENSITIVE_KEYS:
            raise ValueError(f"Access to sensitive data '{key}' is prohibited.")
        try:
            value = context[obj_name].__dict__[attr]
        except (KeyError, AttributeError) as exc:
            raise ValueError(f"Missing data for placeholder '{key}'.") from exc
        return str(value)

    pattern = r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return re.sub(pattern, _replacement, template)

# ----------------------------------------------------------------------
# Main API
# ----------------------------------------------------------------------
def generate_employee_summary(employee_id: str, template: str) -> str:
    """
    Generate a summary string for an employee based on the provided template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        Summary template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted summary string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee or performance record cannot be found, if the template
        contains placeholders for sensitive data (feedback or bonus), or if any
        placeholder refers to missing attributes.
    """
    # Validate input types
    if not isinstance(employee_id, str) or not isinstance(template, str):
        raise ValueError("Both employee_id and template must be strings.")

    # Retrieve data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Build context for placeholder substitution
    context = {
        "employee": employee,
        "performance": performance,
    }

    # Ensure template does not reference sensitive data
    placeholders = _extract_placeholders(template)
    for ph in placeholders:
        if ph in _SENSITIVE_KEYS:
            raise ValueError(f"Template contains disallowed placeholder '{ph}'.")

    # Perform substitution
    return _replace_placeholders(template, context)