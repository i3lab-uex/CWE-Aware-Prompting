import re
from typing import List

# Assuming the Employee class is defined elsewhere in the application.
# For completeness, we provide a minimal stub. In real usage this should be replaced
# by the actual Employee implementation.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = None, personal_email: str = None):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# A global list of all employees. In practice this would come from a database or
# another data source.
EMPLOYEES: List[Employee] = []


def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A string containing placeholders such as `{employee.name}` or
        `{employee.position}` to be replaced with actual employee data.

    Returns
    -------
    str
        The formatted directory string for the selected department.

    Raises
    ------
    ValueError
        If a placeholder refers to sensitive data (`salary` or `personal_email`) or if any error
        occurs during processing.
    """
    # Define the set of attributes that are considered sensitive.
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    # Find all placeholders in the template.
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(dir_template)

    # Ensure no sensitive data is requested.
    if any(field in SENSITIVE_FIELDS for field in placeholders):
        raise ValueError("Attempt to access sensitive employee data is not allowed.")

    # Filter employees belonging to the specified department.
    filtered_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    # Build the directory string by formatting each employee's data.
    lines = []
    for emp in filtered_employees:
        # Prepare a dictionary of allowed attributes.
        context = {
            "name": emp.name,
            "position": emp.position,
            # Add any other non-sensitive attributes that might be used.
        }
        try:
            formatted = dir_template.format(employee=context)
        except Exception as exc:
            # Wrap any formatting errors in a ValueError.
            raise ValueError(f"Error processing template: {exc}") from exc
        lines.append(formatted)

    # Join all formatted lines into a single string.
    return "\n".join(lines)