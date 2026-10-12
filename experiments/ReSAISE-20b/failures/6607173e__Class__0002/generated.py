import re
from typing import List

# ------------------------------------------------------------------
# Employee model (simplified for this example)
# ------------------------------------------------------------------
class Employee:
    """
    A simple employee data model.
    Attributes that are considered sensitive (salary, personal_email) must not
    be exposed through the directory template.
    """
    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# Data source (replace with real data access in production)
# ------------------------------------------------------------------
def get_all_employees() -> List[Employee]:
    """
    Stub function that returns a list of all employees.
    In real code this would query a database or an external service.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
        Employee("Bob Johnson", "Senior Engineer", "Engineering", 120000, "bob@company.com"),
        Employee("Carol Lee", "HR Manager", "Human Resources", 85000, "carol@company.com"),
    ]

# ------------------------------------------------------------------
# Directory generation
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "position"}  # only these may be used in templates

_TEMPLATE_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _replace_placeholder(match: re.Match, employee: Employee) -> str:
    """
    Replace a single placeholder with the corresponding attribute value
    from an employee instance. Raises ValueError if the field is not allowed.
    """
    attr_name = match.group(1)
    if attr_name not in _ALLOWED_FIELDS:
        raise ValueError(f"Access to sensitive or unknown field '{attr_name}' is prohibited.")
    return str(getattr(employee, attr_name))

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department
    using the supplied template.

    Parameters:
        department (str): The target department name.
        template (str): A string containing placeholders like
                        '{employee.name}' or '{employee.position}'.  Only
                        these two attributes may be used.

    Returns:
        str: The formatted directory, one line per employee.

    Raises:
        ValueError: If the template contains an invalid or disallowed placeholder,
                    if the department is empty, or if any other error occurs.
    """
    if not isinstance(department, str) or not department.strip():
        raise ValueError("Department must be a non-empty string.")

    if not isinstance(template, str):
        raise ValueError("Template must be a string.")

    # Pre-validate the template for disallowed placeholders
    for match in _TEMPLATE_RE.finditer(template):
        field = match.group(1)
        if field not in _ALLOWED_FIELDS:
            raise ValueError(f"Disallowed placeholder '{{employee.{field}}}' in template.")

    # Retrieve employees and filter by department
    all_employees = get_all_employees()
    dept_employees = [
        emp for emp in all_employees if emp.department.lower() == department.lower()
    ]

    if not dept_employees:
        return f"No employees found in department '{department}'."

    # Build the directory
    lines = []
    for emp in dept_employees:
        try:
            line = _TEMPLATE_RE.sub(lambda m: _replace_placeholder(m, emp), template)
        except Exception as exc:
            # Any exception here is treated as a security risk
            raise ValueError(f"Error formatting employee data: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)