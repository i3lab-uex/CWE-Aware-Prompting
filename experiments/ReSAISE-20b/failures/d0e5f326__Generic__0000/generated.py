import re
from dataclasses import dataclass, field
from typing import Dict

# ---------- Sample data models ---------------------------------------------

@dataclass
class Employee:
    id: str
    name: str
    department: str
    position: str

@dataclass
class Performance:
    employee_id: str
    rating: float
    feedback: str = field(repr=False)  # sensitive
    bonus: float = field(default=0.0, repr=False)  # sensitive

# ---------- In‑memory "database" -------------------------------------------

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", department="Engineering", position="Senior Engineer"),
    "E002": Employee(id="E002", name="Bob Jones", department="Marketing", position="Marketing Lead"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5, feedback="Excellent problem solving.", bonus=1200),
    "E002": Performance(employee_id="E002", rating=3.8, feedback="Good teamwork.", bonus=800),
}

# ---------- Utility functions ---------------------------------------------

def _validate_placeholders(template: str):
    """
    Ensure the template does not reference unauthorized fields
    (feedback or bonus). Raises ValueError if found.
    """
    # Find all field names in the format string
    pattern = re.compile(r"{([^{}]+)}")
    for match in pattern.finditer(template):
        field_name = match.group(1).strip()
        # Allow nested attributes like staff.name
        if '.' in field_name:
            root, attr = field_name.split('.', 1)
            if root == "evaluation" and attr in {"feedback", "bonus"}:
                raise ValueError(f"Unauthorized access to '{field_name}' in template.")
        else:
            # Direct field names are not expected; treat as error
            raise ValueError(f"Invalid placeholder '{field_name}' in template.")

def _get_employee_and_performance(emp_id: str):
    """
    Retrieve employee and performance objects for a given ID.
    Raises ValueError if the ID is not found.
    """
    employee = EMPLOYEES.get(emp_id)
    if not employee:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.")
    performance = PERFORMANCES.get(emp_id)
    if not performance:
        raise ValueError(f"Performance record for employee ID '{emp_id}' does not exist.")
    return employee, performance

# ---------- Main function -------------------------------------------------

def build_employee_report(employee_id: str, template: str) -> str:
    """
    Build a performance report for the given employee based on a template.
    
    Parameters
    ----------
    employee_id : str
        Unique identifier for the employee.
    template : str
        Template string containing placeholders like '{staff.name}' or
        '{evaluation.rating}'. The template must not reference sensitive fields
        such as 'feedback' or 'bonus'.
    
    Returns
    -------
    str
        The formatted performance summary.
    
    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template contains unauthorized
        placeholders (e.g., 'feedback' or 'bonus').
    """
    # Validate placeholders first to catch unauthorized fields early
    _validate_placeholders(template)

    # Fetch data objects
    employee, performance = _get_employee_and_performance(employee_id)

    # Prepare namespace for formatting
    context = {
        "staff": employee,
        "evaluation": performance,
    }

    try:
        result = template.format(**context)
    except KeyError as exc:
        # A placeholder referenced a missing attribute
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result

# ---------- Example usage (for testing) ------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Employee Report\n"
        "Name: {staff.name}\n"
        "Position: {staff.position}\n"
        "Department: {staff.department}\n"
        "Rating: {evaluation.rating}"
    )
    print(build_employee_report("E001", tmpl))