import re
from typing import List

# Assuming an Employee class is defined elsewhere with the following attributes:
# name, position, department, salary, personal_email
# For type checking purposes we define a minimal protocol.
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# In a real application, this list would come from a database or other data source.
EMPLOYEES: List[Employee] = []

# Regular expression to find placeholders like {employee.name}
PLACEHOLDER_RE = re.compile(r'\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}')

# Set of attributes that are considered sensitive and must not be exposed
SENSITIVE_FIELDS = {'salary', 'personal_email'}


def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted directory string for all employees in the specified division.

    Parameters
    ----------
    division : str
        The department name used to filter employees.
    template_str : str
        A string containing placeholders of the form `{employee.<attribute>}`.

    Returns
    -------
    str
        The directory string with placeholders replaced by employee data, each employee on a new line.

    Raises
    ------
    ValueError
        If the template contains sensitive fields or if any error occurs during processing.
    """
    # Validate that the template does not reference sensitive fields
    try:
        placeholders = PLACEHOLDER_RE.findall(template_str)
        for field in placeholders:
            if field in SENSITIVE_FIELDS:
                raise ValueError(f"Attempt to expose sensitive field '{field}' in template.")
    except Exception as exc:
        raise ValueError(f"Template validation failed: {exc}") from exc

    # Filter employees belonging to the requested division
    try:
        filtered = [emp for emp in EMPLOYEES if getattr(emp, 'department', None) == division]
    except Exception as exc:
        raise ValueError(f"Failed to filter employees: {exc}") from exc

    # Build the directory string
    lines = []
    for emp in filtered:
        try:
            line = template_str.format(employee=emp)
            lines.append(line)
        except Exception as exc:
            raise ValueError(f"Failed to format line for employee '{getattr(emp, 'name', '<unknown>')}': {exc}") from exc

    return "\n".join(lines)