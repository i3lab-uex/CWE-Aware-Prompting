import re
from typing import Dict

# ------------------------------------------------------------------
# Mock data models (in a real system these would be ORM classes)
# ------------------------------------------------------------------

class Employee:
    def __init__(self, code: str, name: str, position: str, department: str):
        self.code = code
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee_code: str, rating: float, feedback: str, bonus: float):
        self.employee_code = employee_code
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# ------------------------------------------------------------------
# In‑memory data store (replace with database lookups in production)
# ------------------------------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Senior Engineer", "R&D"),
    "E002": Employee("E002", "Bob Johnson", "Project Manager", "Operations"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("E001", 4.5, "Excellent problem‑solving skills.", 5000),
    "E002": Performance("E002", 4.2, "Strong leadership.", 4000),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _parse_placeholders(template: str):
    """
    Return a set of placeholders found in the template.
    Placeholders are expected to be in the form {object.attribute}.
    """
    pattern = r"\{([a-zA-Z_][\w\.]*)\}"
    return set(re.findall(pattern, template))

def _get_attribute(obj, attr_path: str):
    """
    Retrieve a nested attribute from an object using dot notation.
    Raise AttributeError if any part of the path does not exist.
    """
    parts = attr_path.split(".")
    value = obj
    for part in parts:
        if not hasattr(value, part):
            raise AttributeError(f"Attribute '{part}' not found in object {value}")
        value = getattr(value, part)
    return value

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a formatted performance report for the given employee.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee or performance data cannot be found, or if a
        restricted field (feedback or bonus) is requested.
    """
    # Retrieve data objects
    employee = EMPLOYEES.get(emp_code)
    performance = PERFORMANCES.get(emp_code)

    if employee is None:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    if performance is None:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.")

    # Parse placeholders
    placeholders = _parse_placeholders(summary_template)

    # Map placeholder names to actual objects
    context_map = {
        "employee": employee,
        "performance": performance,
    }

    # Validate placeholders and build the substitution dict
    substitution: Dict[str, str] = {}
    for placeholder in placeholders:
        if "." not in placeholder:
            raise ValueError(f"Invalid placeholder format: '{{{placeholder}}}'")
        obj_name, attr_path = placeholder.split(".", 1)
        if obj_name not in context_map:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{placeholder}}}'")

        # Disallow access to sensitive fields
        if obj_name == "performance" and attr_path in {"feedback", "bonus"}:
            raise ValueError(f"Access to restricted field '{attr_path}' is not allowed.")

        try:
            value = _get_attribute(context_map[obj_name], attr_path)
        except AttributeError as exc:
            raise ValueError(f"Invalid attribute path '{placeholder}': {exc}") from exc

        substitution[placeholder] = str(value)

    # Perform the formatting
    try:
        formatted_report = summary_template.format(**substitution)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return formatted_report