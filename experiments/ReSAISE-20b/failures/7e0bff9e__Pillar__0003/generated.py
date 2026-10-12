import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Mocked data structures (replace with real implementations)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, code: str, name: str, position: str, department: str):
        self.code = code
        self.name = name
        self.position = position
        self.department = department

class Performance:
    def __init__(self, employee_code: str, rating: float, feedback: str = "", bonus: float = 0.0):
        self.employee_code = employee_code
        self.rating = rating
        self.feedback = feedback
        self.bonus = bonus

# ------------------------------------------------------------------
# Data access layer (replace with real DB/ORM queries)
# ------------------------------------------------------------------
def _fetch_employee(emp_code: str) -> Employee:
    # Dummy implementation – replace with real lookup
    dummy_db = {
        "E001": Employee("E001", "Alice Smith", "Software Engineer", "Engineering"),
        "E002": Employee("E002", "Bob Johnson", "Product Manager", "Product"),
    }
    if emp_code not in dummy_db:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    return dummy_db[emp_code]

def _fetch_performance(emp_code: str) -> Performance:
    # Dummy implementation – replace with real lookup
    dummy_perf = {
        "E001": Performance("E001", rating=4.5),
        "E002": Performance("E002", rating=3.8),
    }
    if emp_code not in dummy_perf:
        raise ValueError(f"Performance data for employee '{emp_code}' not found.")
    return dummy_perf[emp_code]

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a formatted performance report for an employee.

    Parameters
    ----------
    emp_code : str
        Identifier of the employee.
    summary_template : str
        Template string containing placeholders such as
        '{employee.name}', '{performance.rating}'.

    Returns
    -------
    str
        The formatted performance report string.

    Raises
    ------
    ValueError
        If the template references invalid or restricted fields.
    """
    # Allowed mapping of placeholder names to actual values
    employee = _fetch_employee(emp_code)
    performance = _fetch_performance(emp_code)

    allowed_attrs: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Identify all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    for match in placeholder_pattern.finditer(summary_template):
        key = match.group(1).strip()
        if key not in allowed_attrs:
            # Reject any restricted or unknown fields
            raise ValueError(f"Invalid or restricted placeholder '{key}' in template.")
    
    # Perform formatting
    try:
        formatted = summary_template.format(**allowed_attrs)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing data for placeholder '{exc.args[0]}'") from exc
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Error formatting template: {exc}") from exc

    return formatted