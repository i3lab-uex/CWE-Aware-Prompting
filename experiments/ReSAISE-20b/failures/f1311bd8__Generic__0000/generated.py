import re
from dataclasses import dataclass
from typing import Dict, Any

# ------------------------------------------------------------------
# Sample data structures – in a real system these would come from a DB
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Employee:
    id: str
    name: str
    position: str
    department: str

@dataclass(frozen=True)
class Performance:
    employee_id: str
    rating: float
    # Restricted fields (not to be exposed in reports)
    feedback: str
    bonus: float

# ------------------------------------------------------------------
# Mock data store (replace with real persistence in production)
# ------------------------------------------------------------------
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Developer",
                     department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Designer",
                     department="Design"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent teamwork and coding skills.",
                        bonus=1200.0),
    "E002": Performance(employee_id="E002", rating=4.2,
                        feedback="Creative designs, meets deadlines.",
                        bonus=950.0),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with id '{emp_id}' not found") from exc

def _get_performance(emp_id: str) -> Performance:
    """Retrieve performance by employee ID, raising ValueError if not found."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee id '{emp_id}' not found") from exc

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders like '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, or if a
        restricted field such as 'feedback' or 'bonus' is requested.
    """
    # Validate and fetch data
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Allowed fields
    allowed_fields = {
        "employee": {"name", "position", "department"},
        "performance": {"rating"}
    }

    # Find all placeholders
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(template_str):
        key = match.group(1).strip()
        if "." not in key:
            raise ValueError(f"Invalid placeholder format: '{{{key}}}'")

        obj_name, attr = key.split(".", 1)
        if obj_name not in allowed_fields:
            raise ValueError(f"Unknown object '{obj_name}' in placeholder '{{{key}}}'")
        if attr not in allowed_fields[obj_name]:
            raise ValueError(f"Access to restricted field '{attr}' in placeholder '{{{key}}}'")

    # Build a mapping for formatting
    class SafeFormatter(dict):
        def __missing__(self, key: str) -> Any:
            # This should never happen due to validation above
            raise KeyError(f"Missing key: {key}")

    formatter = SafeFormatter(
        employee={
            "name": employee.name,
            "position": employee.position,
            "department": employee.department
        },
        performance={
            "rating": performance.rating
        }
    )

    # Perform formatting
    try:
        report = template_str.format_map(formatter)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = ("Employee: {employee.name}\n"
            "Position: {employee.position}\n"
            "Department: {employee.department}\n"
            "Performance Rating: {performance.rating}")
    print(create_employee_report("E001", tmpl))