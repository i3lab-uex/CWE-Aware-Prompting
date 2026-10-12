import re
from typing import Any, Dict

# ----------------------------------------------------------------------
# Mocked data models (replace with real implementations in production)
# ----------------------------------------------------------------------
class Performance:
    def __init__(self, rating: str, feedback: str = "", bonus: float = 0.0):
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus


class Employee:
    def __init__(
        self,
        emp_id: str,
        name: str,
        position: str,
        department: str,
        performance: Performance,
    ):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department
        self.performance = performance


# ----------------------------------------------------------------------
# In‑memory “database” for demonstration purposes
# ----------------------------------------------------------------------
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Senior Analyst",
        department="Finance",
        performance=Performance(rating="Exceeds Expectations", feedback="Great work on Q1 report.", bonus=1500.0),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Developer",
        department="Engineering",
        performance=Performance(rating="Meets Expectations", feedback="", bonus=0.0),
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """
    Retrieve an employee from the mock database.
    Raises ValueError if the ID is not found.
    """
    try:
        return EMPLOYEE_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{emp_id}' not found.") from exc


def _parse_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {something} from a template.
    Returns a set of placeholder names (e.g., 'employee.name').
    """
    return set(re.findall(r"{([^}]+)}", template))


def _resolve_placeholder(name: str, employee: Employee) -> Any:
    """
    Resolve a single placeholder name against an Employee instance.
    Allowed fields: employee.name, employee.position, employee.department,
                    performance.rating
    Restricted fields: performance.feedback, performance.bonus
    """
    # Split into parts and traverse attributes
    parts = name.split(".")
    if not parts:
        raise ValueError(f"Empty placeholder in template.")

    obj: Any = employee
    for part in parts:
        if not hasattr(obj, part):
            raise ValueError(f"Invalid placeholder '{name}'.")
        obj = getattr(obj, part)

    # Check for restricted fields
    if name in {"performance.feedback", "performance.bonus"}:
        raise ValueError(f"Access to restricted field '{name}' is prohibited.")

    return obj


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee to report on.
    template_str : str
        Template containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The template with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the employee ID is invalid, a placeholder references an unknown
        attribute, or a restricted field is requested.
    """
    # Retrieve employee data
    employee = _get_employee(emp_id)

    # Find all placeholders in the template
    placeholders = _parse_placeholders(template_str)

    # Build a mapping for safe replacement
    values: Dict[str, str] = {}
    for placeholder in placeholders:
        # Map placeholder to a key understood by format()
        # e.g., 'employee.name' -> 'employee_name'
        key = placeholder.replace(".", "_")
        value = _resolve_placeholder(placeholder, employee)
        values[key] = str(value)

    # Replace placeholders using a safe format
    # Convert template to use underscores instead of dots for formatting keys
    safe_template = re.sub(r"{([^}]+)}", lambda m: "{" + m.group(1).replace(".", "_") + "}", template_str)

    try:
        report = safe_template.format(**values)
    except KeyError as exc:
        raise ValueError(f"Missing value for placeholder {exc}") from exc

    return report