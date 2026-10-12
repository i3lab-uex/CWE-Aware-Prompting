import re
from typing import List

# Assuming an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global employee repository (in a real system this would be a database or API)
EMPLOYEES: List[Employee] = []


def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department
    using the provided template.

    Parameters
    ----------
    department : str
        Name of the department to filter employees.
    template : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'. Sensitive data such as 'personal_email'
        is prohibited.

    Returns
    -------
    str
        A string containing one formatted entry per employee, separated by newlines.

    Raises
    ------
    ValueError
        If the template contains disallowed placeholders or if any other error occurs.
    """
    # Disallow sensitive data in the template
    disallowed = {"personal_email"}
    placeholders = set(re.findall(r"{employee\.([a-zA-Z_][a-zA-Z0-9_]*)}", template))
    if disallowed & placeholders:
        raise ValueError("Template contains access to sensitive information.")

    # Filter employees by department
    filtered = [emp for emp in EMPLOYEES if emp.department.lower() == department.lower()]
    if not filtered:
        return ""

    # Prepare the replacement function
    def replace(match: re.Match) -> str:
        attr = match.group(1)
        try:
            value = getattr(emp, attr)
        except AttributeError as exc:
            raise ValueError(f"Invalid attribute '{attr}' in template.") from exc
        # Convert non-string values to string safely
        return str(value)

    directory_entries = []
    for emp in filtered:
        try:
            entry = re.sub(r"{employee\.([a-zA-Z_][a-zA-Z0-9_]*)}",
                           replace, template)
        except Exception as exc:
            raise ValueError(f"Error processing employee '{emp.name}'.") from exc
        directory_entries.append(entry)

    return "\n".join(directory_entries)