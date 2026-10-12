import re
from typing import List

# Assuming an Employee class exists in the environment. For completeness we provide a minimal stub.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# In a real application, the list of employees would come from a database or external source.
EMPLOYEES: List[Employee] = []


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory for all employees belonging to ``dept_name``.

    Parameters
    ----------
    dept_name : str
        The department name to filter employees by.
    format_template : str
        A template string containing placeholders of the form `{employee.field}`.

    Returns
    -------
    str
        A string containing one formatted line per employee, joined by newlines.

    Raises
    ------
    ValueError
        If the template tries to access sensitive data (``salary`` or ``personal_email``)
        or if any other error occurs during formatting.
    """
    # Regular expression to find placeholders like {employee.name}
    placeholder_re = re.compile(r'\{([^}]+)\}')

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dept_name]

    formatted_lines: List[str] = []

    for emp in dept_employees:
        try:
            # Function to replace each placeholder
            def repl(match: re.Match) -> str:
                key = match.group(1).strip()
                # Ensure the placeholder refers to an employee attribute
                if not key.startswith('employee.'):
                    raise ValueError(f"Unsupported placeholder '{key}'. "
                                     f"Only 'employee.*' placeholders are allowed.")
                attr_name = key.split('.', 1)[1]
                if attr_name in ('salary', 'personal_email'):
                    raise ValueError(f"Access to sensitive attribute '{attr_name}' is prohibited.")
                # Retrieve the attribute value
                if not hasattr(emp, attr_name):
                    raise ValueError(f"Employee has no attribute '{attr_name}'.")
                return str(getattr(emp, attr_name))

            formatted_line = placeholder_re.sub(repl, format_template)
            formatted_lines.append(formatted_line)
        except Exception as exc:
            # Convert any exception into a ValueError with context
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc

    return "\n".join(formatted_lines)