import re
from typing import List

# Assume Employee is defined elsewhere in the application.
# Here we provide a minimal placeholder for type checking and testing purposes.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# In a real application this list would be populated from a database or other data source.
EMPLOYEES: List[Employee] = []


def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders like `{employee.name}` or
        `{employee.position}` that will be replaced with actual employee data.

    Returns
    -------
    str
        The formatted directory string containing one entry per employee in the
        specified department.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive attributes (salary or
        personal_email) or if any other error occurs during processing.
    """
    # Define which attributes are considered sensitive and must not be exposed
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    # Regular expression to find all placeholders of the form {employee.<attr>}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    # Find all unique attribute names used in the template
    placeholders = set(placeholder_pattern.findall(dir_template))

    # Check for sensitive fields in the template
    if placeholders & SENSITIVE_FIELDS:
        raise ValueError(
            f"Template contains sensitive fields: {placeholders & SENSITIVE_FIELDS}"
        )

    # Filter employees belonging to the requested department
    dept_employees = [
        emp for emp in EMPLOYEES if emp.department == dept_name
    ]

    # Prepare the final directory string
    try:
        formatted_entries = []
        for emp in dept_employees:
            # Build a dictionary of allowed attributes
            context = {
                attr: getattr(emp, attr)
                for attr in placeholders
                if hasattr(emp, attr)
            }
            # If the template references an attribute that doesn't exist,
            # raise an informative error
            missing_attrs = placeholders - context.keys()
            if missing_attrs:
                raise ValueError(
                    f"Employee '{emp.name}' is missing attributes: {missing_attrs}"
                )
            # Perform the formatting
            entry = dir_template.format(**context)
            formatted_entries.append(entry)

        return "\n".join(formatted_entries)
    except Exception as exc:
        # Wrap any exception in a ValueError to comply with the contract
        raise ValueError(f"Error generating directory: {exc}") from exc