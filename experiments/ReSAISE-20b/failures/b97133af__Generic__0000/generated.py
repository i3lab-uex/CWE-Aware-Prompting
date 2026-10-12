import re
from typing import List

# Assuming the Employee class is defined elsewhere in the codebase.
# For demonstration purposes we provide a minimal stub here.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = 0.0, personal_email: str = ""):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global list of employees (replace with real data source).
EMPLOYEES: List[Employee] = []


def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory string for all employees in the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        The directory string with all placeholders replaced by employee data.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive fields (salary or personal_email),
        or if any other error occurs during formatting.
    """
    # Allowed employee attributes that may appear in the template
    allowed_fields = {"name", "position", "department"}

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(dir_template)

    # Validate that no sensitive fields are referenced
    for ph in placeholders:
        if not ph.startswith("employee."):
            continue  # ignore non-employee placeholders
        field = ph.split(".", 1)[1]
        if field not in allowed_fields:
            raise ValueError(f"Access to sensitive or unsupported field '{field}' is not permitted.")

    # Proxy object that exposes only allowed attributes
    class EmployeeProxy:
        __slots__ = ("_emp",)

        def __init__(self, emp: Employee):
            self._emp = emp

        def __getattr__(self, name: str):
            if name in allowed_fields:
                return getattr(self._emp, name)
            raise AttributeError(f"Attribute '{name}' is not accessible.")

        # Provide a readable representation for debugging
        def __repr__(self):
            return f"<EmployeeProxy name={self._emp.name}>"

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dept_name]

    # Build the directory string
    try:
        lines = []
        for emp in dept_employees:
            proxy = EmployeeProxy(emp)
            line = dir_template.format(employee=proxy)
            lines.append(line)
        return "\n".join(lines)
    except Exception as exc:
        # Wrap any exception in ValueError with a clear message
        raise ValueError(f"Failed to generate directory: {exc}") from exc