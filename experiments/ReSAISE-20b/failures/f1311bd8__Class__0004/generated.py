import re
from typing import Any, Dict

# ------------------------------------------------------------------
# Mock data structures (in a real system these would be ORM models or
# similar persistent objects)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, emp_id: str, name: str, position: str,
                 department: str):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.department = department


class Performance:
    def __init__(self, emp_id: str, rating: float,
                 feedback: str = None, bonus: float = None):
        self.emp_id = emp_id
        self.rating = rating
        self.feedback = feedback          # Sensitive
        self.bonus = bonus                # Sensitive


# ------------------------------------------------------------------
# In‑memory "database" for demonstration purposes
# ------------------------------------------------------------------
EMPLOYEES = {
    'E001': Employee('E001', 'Alice Smith', 'Software Engineer',
                     'Engineering'),
    'E002': Employee('E002', 'Bob Johnson', 'Product Manager',
                     'Product'),
}

PERFORMANCES = {
    'E001': Performance('E001', 4.5, feedback='Excellent work on the new API.',
                         bonus=1500.0),
    'E002': Performance('E002', 3.8, feedback='Great product vision.',
                         bonus=1200.0),
}


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee object or raise ValueError."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with ID '{emp_id}' not found") from exc


def _get_performance(emp_id: str) -> Performance:
    """Retrieve a performance object or raise ValueError."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee '{emp_id}' not found") from exc


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Render an employee performance report using a safe templating
    approach.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template containing placeholders such as '{employee.name}',
        '{performance.rating}', etc.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, or if a
        restricted field (feedback or bonus) is requested.
    """
    # Retrieve data
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Allowed fields
    allowed_fields: Dict[str, Any] = {
        'employee.name': employee.name,
        'employee.position': employee.position,
        'employee.department': employee.department,
        'performance.rating': performance.rating,
    }

    # Find all placeholders
    placeholder_pattern = re.compile(r'\{([^{}]+)\}')
    placeholders = placeholder_pattern.findall(template_str)

    # Validate placeholders and build replacement dict
    replacements: Dict[str, str] = {}
    for key in placeholders:
        if key in allowed_fields:
            replacements[key] = str(allowed_fields[key])
        elif key in ('performance.feedback', 'performance.bonus'):
            # Sensitive fields are not allowed
            raise ValueError(f"Access to restricted field '{key}' is denied")
        else:
            # Unknown placeholder
            raise ValueError(f"Unknown template field '{key}'")

    # Perform the substitution safely
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return replacements[key]

    result = placeholder_pattern.sub(_replace, template_str)
    return result


# ------------------------------------------------------------------
# Example usage (would normally be in a separate test or main block)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee Report for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5.0\n"
    )
    print(create_employee_report('E001', template))