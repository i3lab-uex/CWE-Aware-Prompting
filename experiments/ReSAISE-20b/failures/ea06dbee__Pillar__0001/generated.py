import re
from typing import List

# ----------------------------------------------------------------------
# Dummy Employee class for illustration; in real use this would be imported.
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# Global list of employees – in real code this would come from a database
# or another module. For the purpose of this implementation we keep it
# simple and minimal.
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _validate_template(template: str) -> None:
    """
    Ensure that the template does not request sensitive data.
    Raises ValueError if it does or if a placeholder is malformed.
    """
    # Detect any placeholder that references salary or personal_email
    sensitive = re.compile(r'\{employee\.(salary|personal_email)\}')
    if sensitive.search(template):
        raise ValueError("Template attempts to access sensitive data")

    # Ensure all placeholders are well-formed
    placeholder_pattern = re.compile(r'\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}')
    for match in placeholder_pattern.finditer(template):
        attr = match.group(1)
        if not hasattr(Employee, attr) and attr not in ('name', 'position',
                                                       'department'):
            raise ValueError(f"Template contains unknown attribute '{attr}'")

def _format_employee(emp: Employee, template: str) -> str:
    """
    Format a single employee record using the given template.
    """
    mapping = {
        'name': emp.name,
        'position': emp.position,
        'department': emp.department
    }
    try:
        return template.format(employee=mapping)
    except KeyError as exc:
        raise ValueError(f"Missing attribute in template: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Template formatting error: {exc}") from None

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dep : str
        The department whose employees should be listed.
    format_template : str
        A string template containing placeholders such as
        '{employee.name}', '{employee.position}', etc.

    Returns
    -------
    str
        A string containing one formatted line per employee, separated by newlines.

    Raises
    ------
    ValueError
        If the template tries to access sensitive data, contains malformed
        placeholders, or any other error occurs during formatting.
    """
    # Validate the template once before processing employees
    _validate_template(format_template)

    # Filter employees belonging to the requested department
    relevant = [e for e in EMPLOYEES if e.department == dep]

    # If no employees, return an empty string
    if not relevant:
        return ""

    # Format each employee record safely
    formatted_lines = []
    for emp in relevant:
        line = _format_employee(emp, format_template)
        formatted_lines.append(line)

    # Join with newlines and return
    return "\n".join(formatted_lines)