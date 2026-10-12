import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mocked data structures (replace with real implementations)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position

class Performance:
    def __init__(self, rating: str):
        self.rating = rating

# ----------------------------------------------------------------------
# In‑memory employee store (replace with real data source)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee("E001", "Alice Smith", "Software Engineer"),
    "E002": Employee("E002", "Bob Johnson", "Product Manager"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance("Excellent"),
    "E002": Performance("Satisfactory"),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def get_employee(emp_id: str) -> Employee:
    """Retrieve an employee object by ID."""
    if emp_id not in EMPLOYEES:
        raise ValueError(f"Invalid employee ID: {emp_id}")
    return EMPLOYEES[emp_id]

def get_performance(emp_id: str) -> Performance:
    """Retrieve a performance object by employee ID."""
    if emp_id not in PERFORMANCES:
        raise ValueError(f"No performance data for employee ID: {emp_id}")
    return PERFORMANCES[emp_id]

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the given employee based on a template.
    
    Placeholders supported:
        {staff.name}
        {staff.position}
        {evaluation.rating}
    
    Any attempt to access disallowed fields (e.g. feedback, bonus) will raise a ValueError.
    """
    # Retrieve data
    employee = get_employee(employee_id)
    performance = get_performance(employee_id)

    # Define allowed mapping
    allowed_mapping: Dict[str, Any] = {
        "staff.name": employee.name,
        "staff.position": employee.position,
        "evaluation.rating": performance.rating,
    }

    # Regular expression to find placeholders
    pattern = re.compile(r"\{([^}]+)\}")

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in allowed_mapping:
            raise ValueError(f"Unauthorized placeholder access: {{{key}}}")
        return str(allowed_mapping[key])

    # Perform substitution
    try:
        result = pattern.sub(replace_placeholder, template)
    except ValueError as e:
        # Re‑raise to surface unauthorized access
        raise

    return result

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report:\n"
        "Name: {staff.name}\n"
        "Position: {staff.position}\n"
        "Performance Rating: {evaluation.rating}\n"
    )
    print(build_employee_report("E001", tmpl))