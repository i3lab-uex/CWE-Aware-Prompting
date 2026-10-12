import re
from typing import List

# ----------------------------------------------------------------------
# Assume an Employee class is defined elsewhere in the code base.
# For illustration purposes, we provide a minimal stub here.  In
# production this class will be imported from the real module.
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
# Global employee list (to be populated by the application).
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as
        '{employee.name}' or '{employee.position}'.  The placeholders
        are replaced with the corresponding attribute values of each
        employee in the department.

    Returns
    -------
    str
        A single string containing one formatted entry per employee,
        separated by newline characters.

    Raises
    ------
    ValueError
        If a placeholder attempts to access sensitive data (salary or
        personal_email) or if any other error occurs during formatting.
    """
    # Regex to find placeholders of the form {employee.<attribute>}
    placeholder_pattern = re.compile(r'\{employee\.([^\}]+)\}')

    # Collect all placeholders from the template
    placeholders = placeholder_pattern.findall(dir_template)

    # Security check: disallow sensitive attributes
    sensitive_attrs = {'salary', 'personal_email'}
    for attr in placeholders:
        if attr in sensitive_attrs:
            raise ValueError(f"Attempt to expose sensitive attribute '{attr}'")

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dept_name]

    # Prepare formatted lines
    formatted_lines = []

    for employee in dept_employees:
        entry = dir_template
        try:
            # Replace each placeholder with the actual attribute value
            for attr in placeholders:
                if not hasattr(employee, attr):
                    raise ValueError(f"Employee has no attribute '{attr}'")
                value = getattr(employee, attr)
                # Ensure the replacement is string-safe
                entry = re.sub(r'\{employee\.' + re.escape(attr) + r'\}',
                               str(value), entry, count=1)
        except Exception as exc:
            raise ValueError(f"Failed to format entry for employee '{employee.name}': {exc}") from exc

        formatted_lines.append(entry)

    return "\n".join(formatted_lines)