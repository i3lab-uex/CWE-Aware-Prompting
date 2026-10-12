import re
from typing import List

# Example Employee class; in real usage this would be imported from the project.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example data store – replace with the real source of employees.
EMPLOYEES: List[Employee] = []

# -------------------------------------------------------------

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dep : str
        Department name to filter employees by.
    format_template : str
        Template containing placeholders like '{employee.name}' or
        '{employee.position}'. Placeholders for sensitive fields
        ('salary', 'personal_email') are not allowed.

    Returns
    -------
    str
        Concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If a sensitive field is referenced in the template or if any error
        occurs during formatting.
    """
    # Identify all placeholders in the format template
    placeholder_pattern = re.compile(r'\{([^}]+)\}')
    placeholders = placeholder_pattern.findall(format_template)

    # Detect any disallowed fields
    disallowed_fields = {'salary', 'personal_email'}
    for ph in placeholders:
        # Expected format: employee.field
        parts = ph.split('.')
        if len(parts) != 2 or parts[0] != 'employee':
            raise ValueError(f"Invalid placeholder format: {{{ph}}}")
        field_name = parts[1]
        if field_name in disallowed_fields:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dep]
    if not dept_employees:
        return f"No employees found in department '{dep}'."

    # Prepare the final directory string
    lines = []
    for emp in dept_employees:
        try:
            # Build a context dictionary with the employee instance
            context = {'employee': emp}
            line = format_template.format(**context)
            lines.append(line)
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc

    return "\n".join(lines)