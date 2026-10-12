import re
from typing import Dict

# --------------------------------------------------------------------
# Assume the following classes and data store are defined elsewhere in
# the application.  They are included here only for type‑checking and to
# make this example self‑contained.
# --------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str, feedback: str = "", bonus: float = 0.0):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.feedback = feedback          # Sensitive
        self.bonus = bonus                # Sensitive

class Performance:
    def __init__(self, emp_id: str, rating: str):
        self.emp_id = emp_id
        self.rating = rating

# Example in‑memory data store (replace with real persistence layer)
EMPLOYEES: Dict[str, Employee] = {}
PERFORMANCES: Dict[str, Performance] = {}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    emp = EMPLOYEES.get(emp_id)
    if not emp:
        raise ValueError(f"Employee ID '{emp_id}' is invalid.")
    return emp

def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance record by employee ID, raising ValueError if not found."""
    perf = PERFORMANCES.get(emp_id)
    if not perf:
        raise ValueError(f"No performance record found for employee ID '{emp_id}'.")
    return perf

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the given employee using the provided
    template.  Placeholders in the template are of the form:
        {staff.name}
        {staff.position}
        {evaluation.rating}

    Sensitive data such as feedback or bonus are not allowed in the template.
    """
    # Retrieve data
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Mapping of placeholder names to their values
    mapping: Dict[str, str] = {
        "staff.name": employee.name,
        "staff.position": employee.position,
        "staff.department": employee.department,
        "evaluation.rating": performance.rating
    }

    # Detect any placeholder that references sensitive data
    forbidden_attrs = {"feedback", "bonus"}
    placeholders = re.findall(r"\{([^}]+)\}", template)
    for placeholder in placeholders:
        namespace, _, attr = placeholder.partition(".")
        if attr in forbidden_attrs:
            raise ValueError(f"Unauthorized access to sensitive attribute '{attr}'.")

    # Replace placeholders safely
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        if key not in mapping:
            raise ValueError(f"Unknown placeholder '{{{key}}}' in template.")
        return str(mapping[key])

    result = re.sub(r"\{([^}]+)\}", replacer, template)
    return result