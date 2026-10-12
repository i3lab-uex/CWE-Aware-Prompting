import re
from dataclasses import dataclass

# --- Sample data structures (would normally be provided by the system) ---

@dataclass
class Employee:
    name: str
    position: str
    department: str
    # Sensitive fields (not exposed)
    feedback: str = ""
    bonus: float = 0.0

@dataclass
class Performance:
    rating: str
    # Sensitive fields (not exposed)
    feedback: str = ""
    bonus: float = 0.0

# --- Core implementation ---

def build_employee_summary(emp_key: str, template_str: str) -> str:
    """
    Build a formatted employee performance summary.

    Parameters
    ----------
    emp_key : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        Formatted summary string.

    Raises
    ------
    ValueError
        If the template references invalid or restricted data.
    """
    # --------------------------------------------------------------------
    # In a real system, this function would retrieve the employee and
    # performance objects from a database or other data source. For this
    # example we simply create dummy instances.
    # --------------------------------------------------------------------
    employee = _get_employee(emp_key)
    performance = _get_performance(emp_key)

    # --------------------------------------------------------------------
    # Allowed fields mapping
    # --------------------------------------------------------------------
    allowed_fields = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # --------------------------------------------------------------------
    # Validate placeholders
    # --------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{([^\}]+)\}")
    for match in placeholder_pattern.finditer(template_str):
        key = match.group(1).strip()
        # Reject any reference to restricted fields
        if key in ("employee.feedback", "employee.bonus",
                   "performance.feedback", "performance.bonus"):
            raise ValueError(f"Access to restricted field '{key}' is not allowed.")
        # Reject unknown placeholders
        if key not in allowed_fields:
            raise ValueError(f"Unknown placeholder '{key}' in template.")

    # --------------------------------------------------------------------
    # Build the formatted string
    # --------------------------------------------------------------------
    try:
        result = template_str.format(**allowed_fields)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result


# --------------------------------------------------------------------
# Helper functions (mocked for demonstration purposes)
# --------------------------------------------------------------------

def _get_employee(emp_key: str) -> Employee:
    """
    Mock function to retrieve an employee by key.
    Replace with actual data access logic.
    """
    # Example data; in real code, fetch from DB
    dummy_employees = {
        "E001": Employee(name="Alice Smith", position="Software Engineer",
                         department="Engineering", feedback="Great work!", bonus=5000),
        "E002": Employee(name="Bob Johnson", position="Product Manager",
                         department="Product", feedback="Excellent leadership!", bonus=7000),
    }
    if emp_key not in dummy_employees:
        raise ValueError(f"Employee with key '{emp_key}' not found.")
    return dummy_employees[emp_key]


def _get_performance(emp_key: str) -> Performance:
    """
    Mock function to retrieve performance data by employee key.
    Replace with actual data access logic.
    """
    # Example data; in real code, fetch from DB
    dummy_performance = {
        "E001": Performance(rating="Excellent", feedback="Outstanding performance.", bonus=1200),
        "E002": Performance(rating="Good", feedback="Consistent results.", bonus=800),
    }
    if emp_key not in dummy_performance:
        raise ValueError(f"Performance data for employee '{emp_key}' not found.")
    return dummy_performance[emp_key]