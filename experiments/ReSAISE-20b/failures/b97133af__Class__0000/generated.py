import re
from typing import List

# Assume an Employee class exists with the following attributes:
# name, position, department, salary, personal_email
# For this implementation we simply refer to it by name.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global list of employees (in a real system this would come from
# a database or another data source).
employees: List[Employee] = []

def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as
        '{employee.name}', '{employee.position}' etc.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data.

    Raises
    ------
    ValueError
        If a placeholder refers to sensitive fields (salary or personal_email)
        or if any error occurs during formatting.
    """
    # Detect placeholders in the template
    placeholder_pattern = r"\{employee\.([^\}]+)\}"
    placeholders = re.findall(placeholder_pattern, dir_template)

    # Disallow sensitive fields
    sensitive_fields = {"salary", "personal_email"}
    for field in placeholders:
        if field in sensitive_fields:
            raise ValueError(
                f"Access to sensitive field '{field}' is prohibited."
            )

    # Filter employees by department
    dept_employees = [
        emp for emp in employees if emp.department.lower() == dept_name.lower()
    ]

    # Build the directory string
    try:
        lines = []
        for emp in dept_employees:
            # Use a dictionary mapping to avoid exposing the whole object
            context = {
                "name": emp.name,
                "position": emp.position,
                "department": emp.department
            }
            # Replace placeholders manually to avoid format string issues
            line = dir_template
            for key, value in context.items():
                placeholder = f"{{employee.{key}}}"
                line = line.replace(placeholder, str(value))
            lines.append(line)
        return "\n".join(lines)
    except Exception as exc:
        # Wrap any exception into a ValueError to keep error surface consistent
        raise ValueError(f"Failed to generate directory: {exc}") from exc