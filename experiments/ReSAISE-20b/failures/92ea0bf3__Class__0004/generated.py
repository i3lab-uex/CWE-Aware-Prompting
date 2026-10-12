import re
from typing import Dict, Any

# ------------------------------------------------------------------
# Sample data structures (replace with real implementations)
# ------------------------------------------------------------------

class Employee:
    def __init__(self, name: str, position: str, department: str,
                 feedback: str = None, bonus: float = 0.0):
        self.name = name
        self.position = position
        self.department = department
        self.feedback = feedback      # Restricted field
        self.bonus = bonus            # Restricted field

class Performance:
    def __init__(self, rating: str):
        self.rating = rating

# Example in‑memory stores (replace with DB access in real code)
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("Alice Smith", "Senior Engineer", "R&D",
                     feedback="Excellent teamwork.", bonus=1500.0),
    "E002": Employee("Bob Jones", "Project Manager", "Operations",
                     feedback="Needs improvement in time management.", bonus=1200.0),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("A"),
    "E002": Performance("B+"),
}

# ------------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------------

def _allowed_attributes() -> Dict[str, set]:
    """
    Return a mapping of allowed object names to the set of attribute
    names that may be accessed in the template.
    """
    return {
        "employee": {"name", "position", "department"},
        "performance": {"rating"},
    }

def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {object.attribute} from the template.
    """
    pattern = re.compile(r"\{([^{}]+)\}")
    return set(pattern.findall(template))

def _validate_placeholder(placeholder: str, allowed_attrs: Dict[str, set]) -> None:
    """
    Ensure that the placeholder references an allowed attribute.
    Raises ValueError if not permitted or malformed.
    """
    try:
        obj_name, attr = placeholder.split(".", 1)
    except ValueError:
        raise ValueError(f"Malformed placeholder: {{{placeholder}}}")

    if obj_name not in allowed_attrs:
        raise ValueError(f"Unknown object '{obj_name}' in placeholder {{{placeholder}}}")

    if attr not in allowed_attrs[obj_name]:
        raise ValueError(f"Access to restricted or unknown attribute '{attr}' in {{{placeholder}}}")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the employee key is invalid or a restricted field is requested.
    """
    # Retrieve data
    employee = EMPLOYEES.get(emp_key)
    performance = PERFORMANCES.get(emp_key)

    if employee is None:
        raise ValueError(f"Employee key '{emp_key}' not found.")
    if performance is None:
        raise ValueError(f"Performance data for employee key '{emp_key}' not found.")

    # Validate placeholders
    allowed_attrs = _allowed_attributes()
    placeholders = _extract_placeholders(template_str)

    for ph in placeholders:
        _validate_placeholder(ph, allowed_attrs)

    # Build context dictionary for formatting
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Perform the formatting
    try:
        result = template_str.format(**context)
    except KeyError as exc:
        # Should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing value for placeholder {exc}") from exc

    return result

# ------------------------------------------------------------------
# Example usage
# ------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = (
        "Employee Summary:\n"
        "- Name: {employee.name}\n"
        "- Position: {employee.position}\n"
        "- Department: {employee.department}\n"
        "- Performance Rating: {performance.rating}"
    )
    print(build_employee_summary("E001", tmpl))