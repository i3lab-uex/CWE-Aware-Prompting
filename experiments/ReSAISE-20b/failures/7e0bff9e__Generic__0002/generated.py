import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data models
# ----------------------------------------------------------------------
@dataclass
class Employee:
    code: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_code: str
    rating: float
    feedback: str = field(repr=False)  # sensitive, should not be exposed
    bonus: float = field(repr=False)   # sensitive, should not be exposed

# ----------------------------------------------------------------------
# In‑memory data store (for demonstration purposes)
# ----------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(code="E001", name="Alice Smith", position="Developer", department="Engineering"),
    "E002": Employee(code="E002", name="Bob Johnson", position="Manager", department="Sales"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_code="E001", rating=4.5, feedback="Excellent problem solving.", bonus=1200),
    "E002": Performance(employee_code="E002", rating=3.8, feedback="Good leadership.", bonus=800),
}

# ----------------------------------------------------------------------
# Utility: allowed fields
# ----------------------------------------------------------------------
ALLOWED_EMP_FIELDS = {"name", "position", "department"}
ALLOWED_PERF_FIELDS = {"rating"}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Create a formatted performance report for the employee identified by `emp_code`.
    
    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders such as '{employee.name}', 
        '{performance.rating}'. Restricted fields like feedback or bonus cannot
        be requested.
    
    Returns
    -------
    str
        Formatted performance report string.
    
    Raises
    ------
    ValueError
        If the employee or performance record is missing, or if a restricted 
        field is requested in the template.
    """
    # Fetch data
    employee = EMPLOYEES.get(emp_code)
    if not employee:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    performance = PERFORMANCES.get(emp_code)
    if not performance:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.")

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = placeholder_pattern.findall(summary_template)

    # Prepare a mapping for allowed values
    context: Dict[str, any] = {}
    for placeholder in placeholders:
        # Normalize: remove leading/trailing whitespace
        key = placeholder.strip()
        if key.startswith("employee."):
            attr = key[len("employee.") :]
            if attr not in ALLOWED_EMP_FIELDS:
                raise ValueError(f"Access to restricted employee field '{attr}' is not allowed.")
            context[key] = getattr(employee, attr)
        elif key.startswith("performance."):
            attr = key[len("performance.") :]
            if attr not in ALLOWED_PERF_FIELDS:
                raise ValueError(f"Access to restricted performance field '{attr}' is not allowed.")
            context[key] = getattr(performance, attr)
        else:
            raise ValueError(f"Unknown placeholder '{key}'.")
    
    # Perform safe formatting
    try:
        report = summary_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing value for placeholder: {exc}") from exc
    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} ({employee.department})\n"
        "Performance Rating: {performance.rating}\n"
    )
    print(create_performance_report("E001", template))