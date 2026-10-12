import re
from typing import List

# ------------------------------------------------------------------
#  Sample Employee class (the real project will provide its own)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
#  Global employee list (replace with the real data source)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ------------------------------------------------------------------
#  Helper to safely format a single employee
# ------------------------------------------------------------------
def _format_employee(employee: Employee, template: str) -> str:
    """
    Replace placeholders in *template* with values from *employee*.
    Raises ValueError if a sensitive attribute is requested or any
    other formatting error occurs.
    """
    # Find all placeholders of the form {employee.attr}
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = pattern.findall(template)

    # Disallow sensitive attributes
    forbidden = {"salary", "personal_email"}
    for attr in placeholders:
        if attr in forbidden:
            raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed")

    # Build a mapping of allowed attributes
    attrs = {attr: getattr(employee, attr) for attr in placeholders}

    try:
        return template.format(**attrs)
    except Exception as exc:
        # Any formatting error is treated as a failure
        raise ValueError(f"Failed to format employee '{employee.name}': {exc}") from exc

# ------------------------------------------------------------------
#  Main function
# ------------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory for all employees belonging to
    *dept_name* using *dir_template*.

    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    dir_template : str
        Template string containing placeholders like {employee.name}
        or {employee.position}.

    Returns
    -------
    str
        A newline‑separated string containing the formatted directory
        entries for each employee in the specified department.

    Raises
    ------
    ValueError
        If a sensitive attribute is accessed, or if any other error
        occurs during formatting.
    """
    # Filter employees by department (case‑insensitive match)
    selected = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]

    # If no employees found, return an empty string
    if not selected:
        return ""

    formatted_entries = []
    for emp in selected:
        entry = _format_employee(emp, dir_template)
        formatted_entries.append(entry)

    # Join entries with newline
    return "\n".join(formatted_entries)