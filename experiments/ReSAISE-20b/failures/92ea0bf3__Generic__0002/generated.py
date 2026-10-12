import re
from typing import Any

# ----------------------------------------------------------------------
# Assume these classes are defined elsewhere in the application.
# They are shown here only for type checking and documentation purposes.

class Employee:
    def __init__(self, name: str, position: str, department: str):
        self.name = name
        self.position = position
        self.department = department
        # restricted fields
        self.feedback: str | None = None
        self.bonus: float | None = None

class Performance:
    def __init__(self, rating: str, goals_met: int, projects_completed: int):
        self.rating = rating
        self.goals_met = goals_met
        self.projects_completed = projects_completed
        # restricted fields
        self.feedback: str | None = None
        self.bonus: float | None = None

# ----------------------------------------------------------------------
# Helper functions that would normally retrieve data from a database or
# other persistent storage.  For this example they simply raise an error.
def get_employee(emp_key: str) -> Employee:
    """Retrieve the Employee instance for a given key."""
    raise NotImplementedError("Employee retrieval not implemented")

def get_performance(emp_key: str) -> Performance:
    """Retrieve the Performance instance for a given key."""
    raise NotImplementedError("Performance retrieval not implemented")

# ----------------------------------------------------------------------
def _get_attr(obj: Any, attr_name: str) -> Any:
    """
    Safely get an attribute from an object.
    Raises ValueError if the attribute is restricted or does not exist.
    """
    # Restricted fields that should never be exposed
    RESTRICTED = {"feedback", "bonus"}

    if not hasattr(obj, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on {obj.__class__.__name__}")

    if attr_name in RESTRICTED:
        raise ValueError(f"Access to restricted field '{attr_name}' is not allowed")

    return getattr(obj, attr_name)

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary based on the supplied template.

    Placeholders are of the form `{entity.attribute}` where entity is either
    `employee` or `performance`.  Restricted attributes (`feedback`, `bonus`)
    are prohibited and will raise a ValueError.

    Parameters
    ----------
    emp_key : str
        Identifier for the employee.
    template_str : str
        Template string containing placeholders.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If a placeholder refers to an invalid attribute or a restricted field.
    """
    # Retrieve data objects
    employee = get_employee(emp_key)
    performance = get_performance(emp_key)

    # Regex to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{([^}]+)\}")

    def replace_match(match: re.Match) -> str:
        expr = match.group(1).strip()
        if "." not in expr:
            raise ValueError(f"Invalid placeholder format: '{{{expr}}}'")
        entity_name, attr_name = expr.split(".", 1)

        if entity_name == "employee":
            value = _get_attr(employee, attr_name)
        elif entity_name == "performance":
            value = _get_attr(performance, attr_name)
        else:
            raise ValueError(f"Unknown entity '{entity_name}' in placeholder '{{{expr}}}'")

        return str(value)

    # Perform all substitutions
    result = placeholder_pattern.sub(replace_match, template_str)
    return result