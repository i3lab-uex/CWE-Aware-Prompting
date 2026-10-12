import re
from typing import List

# Assuming Employee is defined elsewhere in the project.
# Example minimal definition for context (commented out):
#
# class Employee:
#     def __init__(self, name: str, position: str, department: str,
#                  salary: float, personal_email: str):
#         self.name = name
#         self.position = position
#         self.department = department
#         self.salary = salary
#         self.personal_email = personal_email

def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    format_template : str
        A template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If the template tries to access restricted fields (salary or personal_email)
        or if an error occurs during formatting.
    """
    # Define the set of disallowed placeholders
    DISALLOWED = {"salary", "personal_email"}

    # Find all placeholder names inside the template
    placeholders = re.findall(r"{employee\.([a-zA-Z_][a-zA-Z0-9_]*)}", format_template)

    # If any placeholder is disallowed, raise an error
    if any(name in DISALLOWED for name in placeholders):
        raise ValueError("Access to sensitive employee data is prohibited.")

    # Prepare the list of allowed attributes
    ALLOWED_ATTRS = {name for name in placeholders}

    # Filter employees by department
    dept_employees: List[Employee] = [
        e for e in Employee.get_all() if e.department == dept_name
    ]

    # Build the directory lines
    lines = []
    for emp in dept_employees:
        try:
            # Create a mapping of allowed attributes
            context = {attr: getattr(emp, attr) for attr in ALLOWED_ATTRS}
            line = format_template.format(employee=context)
            lines.append(line)
        except Exception as exc:
            raise ValueError(f"Failed to format employee data: {exc}") from exc

    return "\n".join(lines)