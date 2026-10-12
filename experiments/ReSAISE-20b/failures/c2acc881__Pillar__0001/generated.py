import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# Example:
# class Employee:
#     def __init__(self, name, position, department, salary, personal_email):
#         self.name = name
#         self.position = position
#         self.department = department
#         self.salary = salary
#         self.personal_email = personal_email

def compile_department_roster(division: str, template_str: str) -> str:
    """
    Build a formatted employee directory for the specified division.

    Parameters
    ----------
    division : str
        The department name used to filter employees.
    template_str : str
        A string containing placeholders of the form {employee.<attribute>}.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data.

    Raises
    ------
    ValueError
        If a sensitive attribute is accessed or any other error occurs.
    """
    # Regular expression to capture placeholders like {employee.name}
    placeholder_pattern = re.compile(r'\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}')

    # Sensitive attributes that must not be exposed
    SENSITIVE_ATTRS = {'salary', 'personal_email'}

    # Gather employees from the global scope or any provided collection
    try:
        all_employees: List[object] = globals().get('EMPLOYEES', [])
    except Exception as exc:
        raise ValueError(f"Failed to access employee collection: {exc}") from exc

    # Filter employees by division
    department_employees = [
        emp for emp in all_employees if getattr(emp, 'department', None) == division
    ]

    rendered_lines = []

    for emp in department_employees:
        # Function to replace a single placeholder
        def repl(match):
            attr = match.group(1)
            if attr in SENSITIVE_ATTRS:
                raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
            try:
                value = getattr(emp, attr)
            except AttributeError as exc:
                raise ValueError(f"Employee has no attribute '{attr}'.") from exc
            return str(value)

        try:
            rendered = placeholder_pattern.sub(repl, template_str)
        except Exception as exc:
            raise ValueError(f"Error rendering template for employee '{emp}': {exc}") from exc

        rendered_lines.append(rendered)

    return "\n".join(rendered_lines)