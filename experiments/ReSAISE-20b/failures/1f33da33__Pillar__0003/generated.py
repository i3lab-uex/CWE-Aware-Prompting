import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Mock data structures (in a real system these would come from a database)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str

@dataclass
class Performance:
    emp_id: str
    rating: float
    feedback: str   # Restricted
    bonus: float    # Restricted

# In‑memory "database"
_EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(emp_id="E002", name="Bob Jones", position="Project Manager", department="Operations"),
}

_PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5, feedback="Excellent leadership.", bonus=1200),
    "E002": Performance(emp_id="E002", rating=3.8, feedback="Good communication.", bonus=800),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID or raise ValueError."""
    try:
        return _EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {emp_id}") from exc

def _get_performance(emp_id: str) -> Performance:
    """Retrieve performance data by employee ID or raise ValueError."""
    try:
        return _PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"No performance data for employee ID: {emp_id}") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the given employee ID using the supplied template.
    
    The template may contain placeholders in the form '{employee.<attr>}' or
    '{performance.<attr>}'. The following attributes are allowed:
    
      * employee: name, position, department
      * performance: rating
    
    Any attempt to reference restricted fields (feedback or bonus) or an
    invalid employee ID will raise ValueError.
    
    Args:
        emp_id: Unique identifier of the employee.
        summary_template: Template string with placeholders.
    
    Returns:
        A fully formatted summary string.
    """
    # Validate template syntax and collect placeholder names
    placeholder_pattern = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")
    placeholders = placeholder_pattern.findall(summary_template)

    # Prepare mapping for safe formatting
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Allowed fields
    allowed_employee_fields = {"name", "position", "department"}
    allowed_performance_fields = {"rating"}

    mapping: Dict[str, str] = {}

    for key in placeholders:
        if "." not in key:
            raise ValueError(f"Invalid placeholder format: {{{key}}}")
        obj, attr = key.split(".", 1)

        if obj == "employee":
            if attr not in allowed_employee_fields:
                raise ValueError(f"Access to restricted or unknown employee field '{attr}'")
            mapping[key] = str(getattr(employee, attr))
        elif obj == "performance":
            if attr not in allowed_performance_fields:
                raise ValueError(f"Access to restricted or unknown performance field '{attr}'")
            mapping[key] = str(getattr(performance, attr))
        else:
            raise ValueError(f"Unknown placeholder object '{obj}' in {{{key}}}")

    # Perform formatting
    try:
        summary = summary_template.format(**mapping)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing value for placeholder: {exc}") from exc

    return summary

# ----------------------------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Employee {employee.name} ({employee.position}) in {employee.department} achieved a rating of {performance.rating}."
#     print(create_performance_summary("E001", tmpl))