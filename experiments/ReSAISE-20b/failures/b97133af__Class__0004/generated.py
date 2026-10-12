import re
from typing import List, Any
from string import Formatter

# Minimal Employee definition for illustration. In real usage this would be provided elsewhere.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Simulated employee repository (replace with real data source)
EMPLOYEE_DB: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@corp.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob.johnson@corp.com"),
    Employee("Carol Lee", "Analyst", "Finance", 75000.0, "carol.lee@corp.com"),
    # ... more employees
]

# Set of attributes that are considered sensitive
SENSITIVE_FIELDS = {"salary", "personal_email"}

def _extract_placeholders(template: str) -> List[str]:
    """
    Extract all field names from the template string.
    Raises ValueError if a sensitive field is referenced.
    """
    formatter = Formatter()
    fields = []
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:  # non-empty
            # Support nested attributes like employee.name
            base, _, attr = field_name.partition('.')
            if attr in SENSITIVE_FIELDS:
                raise ValueError(f"Attempt to expose sensitive information: '{field_name}'")
            fields.append(field_name)
    return fields

def _render_employee(template: str, employee: Employee) -> str:
    """
    Render the template for a single employee.
    """
    # Build a mapping from placeholder names to values
    mapping = {}
    formatter = Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if not field_name:
            continue
        # Handle nested attributes (e.g., employee.name)
        parts = field_name.split('.')
        if len(parts) == 1:
            # Direct attribute of Employee
            attr = parts[0]
        else:
            # e.g., employee.name -> use the second part
            attr = parts[-1]
        if not hasattr(employee, attr):
            raise ValueError(f"Unknown attribute '{attr}' in template.")
        mapping[field_name] = getattr(employee, attr)
    try:
        return template.format(**mapping)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format template: {exc}") from exc

def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as '{employee.name}' or
        '{employee.position}'. Sensitive fields like salary or personal_email are
        prohibited.

    Returns
    -------
    str
        The formatted directory string for all employees in the department.

    Raises
    ------
    ValueError
        If a sensitive field is referenced in the template or any error occurs
        during processing.
    """
    if not isinstance(dept_name, str) or not isinstance(dir_template, str):
        raise ValueError("Both dept_name and dir_template must be strings.")

    # Validate template for sensitive fields
    _extract_placeholders(dir_template)

    # Filter employees by department (case‑insensitive match)
    dept_employees = [
        emp for emp in EMPLOYEE_DB if emp.department.lower() == dept_name.lower()
    ]

    if not dept_employees:
        return f"No employees found in department '{dept_name}'."

    rendered_lines = []
    for emp in dept_employees:
        try:
            line = _render_employee(dir_template, emp)
            rendered_lines.append(line)
        except ValueError as exc:  # pragma: no cover
            raise ValueError(f"Error rendering employee {emp.name}: {exc}") from exc

    return "\n".join(rendered_lines)