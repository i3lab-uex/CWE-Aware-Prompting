import re
from typing import List

# Assume an Employee class exists with the following attributes:
# name, position, department, salary, personal_email
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# For the purpose of this implementation we maintain a global list
# of all employees. In real scenarios this could be replaced by a DB query.
ALL_EMPLOYEES: List[Employee] = []

def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division : str
        Department name to filter employees.
    template_str : str
        Directory template containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The formatted directory string for the selected department.

    Raises
    ------
    ValueError
        If a sensitive attribute (salary or personal_email) is requested,
        or if any other error occurs during processing.
    """
    sensitive_attrs = {"salary", "personal_email"}

    # Compile regex to find all placeholders of the form {employee.attr}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    try:
        # Filter employees belonging to the requested division
        department_employees = [
            emp for emp in ALL_EMPLOYEES if emp.department == division
        ]

        # Prepare a list to hold formatted lines for each employee
        formatted_lines = []

        for emp in department_employees:
            # Function to replace each placeholder with the employee's attribute
            def replacer(match):
                attr_name = match.group(1)
                if attr_name in sensitive_attrs:
                    raise ValueError(
                        f"Access to sensitive attribute '{attr_name}' is prohibited."
                    )
                # Retrieve the attribute; raise if it does not exist
                try:
                    value = getattr(emp, attr_name)
                except AttributeError as e:
                    raise ValueError(
                        f"Employee has no attribute '{attr_name}'."
                    ) from e
                return str(value)

            # Apply replacements on the template string
            formatted_line = placeholder_pattern.sub(replacer, template_str)
            formatted_lines.append(formatted_line)

        # Join all lines with a newline separator
        return "\n".join(formatted_lines)

    except Exception as exc:
        # Any exception is wrapped into a ValueError for consistency
        raise ValueError(f"Failed to compile roster: {exc}") from exc