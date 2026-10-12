import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Domain model (minimal implementation for the example)
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
    """Represents performance data for an employee."""
    emp_id: str
    rating: float
    # Sensitive fields – must never be exposed via the template
    feedback: str = field(repr=False)
    bonus: float = field(repr=False)

# --------------------------------------------------------------------------- #
# In‑memory data store (replace with real persistence in production)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=5000),
    "E002": Performance(emp_id="E002", rating=3.8, feedback="Good leadership.", bonus=3000),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{(?P<scope>\w+)\.(?P<attr>\w+)\}")

# Fields that are considered sensitive and must not be exposed via the template
RESTRICTED_FIELDS = {"feedback", "bonus"}

def _get_attribute(scope: str, attr: str):
    """
    Resolve an attribute from the given scope.
    Raises ValueError if the attribute is restricted or does not exist.
    """
    if scope == "employee":
        obj = EMPLOYEES.get(current_emp_id)
    elif scope == "performance":
        obj = PERFORMANCES.get(current_emp_id)
    else:
        raise ValueError(f"Unknown scope '{scope}' in placeholder.")

    if obj is None:
        raise ValueError(f"No data found for employee ID '{current_emp_id}'.")

    if attr in RESTRICTED_FIELDS:
        raise ValueError(f"Access to restricted field '{attr}' is not allowed.")

    if not hasattr(obj, attr):
        raise ValueError(f"Attribute '{attr}' does not exist in {scope} data.")

    return getattr(obj, attr)

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee to generate a report for.
    template_str : str
        A string containing placeholders in the form `{scope.attribute}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, if a restricted field is requested,
        or if an attribute does not exist.
    """
    global current_emp_id
    current_emp_id = emp_id  # used by _get_attribute to resolve data

    if emp_id not in EMPLOYEES:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")

    # Find all placeholders
    placeholders = PLACEHOLDER_PATTERN.findall(template_str)

    # Validate and replace each placeholder
    result = template_str
    for scope, attr in placeholders:
        value = _get_attribute(scope, attr)
        # Use simple string replacement; placeholders are unique
        result = result.replace(f"{{{scope}.{attr}}}", str(value))

    return result

# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report for {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}"
    )
    print(create_employee_report("E001", tmpl))