import string
from typing import List, Any

# ----------------------------------------------------------------------
# Assume an Employee class is defined somewhere in the code base.
# For demonstration purposes we provide a minimal implementation below.
# ----------------------------------------------------------------------
class Employee:
    """
    Simple employee data container.
    Sensitive attributes are `salary` and `personal_email`.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# Global list of employees. In a real application this would be
# replaced by a database query or another data source.
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory for all employees in `dept_name`.

    Parameters
    ----------
    dept_name : str
        The department name to filter employees.
    dir_template : str
        A template string containing placeholders such as `{employee.name}`.

    Returns
    -------
    str
        The concatenated formatted directory entries, one per line.

    Raises
    ------
    ValueError
        If the template references sensitive attributes (`salary`,
        `personal_email`) or if any error occurs during formatting.
    """
    # --- Validation of template placeholders --------------------------------
    formatter = string.Formatter()
    sensitive_fields = {"salary", "personal_email"}

    for _, field_name, _, _ in formatter.parse(dir_template):
        if field_name is None:
            continue
        # Field names may contain nested attributes like 'employee.name'.
        # Split by '.' and consider the last component as the attribute.
        attr = field_name.split(".")[-1]
        if attr in sensitive_fields:
            raise ValueError(f"Access to sensitive field '{attr}' is not allowed.")

    # --- Filter employees by department ------------------------------------
    filtered = [emp for emp in EMPLOYEES if emp.department == dept_name]

    # --- Prepare formatted entries ------------------------------------------
    entries: List[str] = []
    for emp in filtered:
        # Build a mapping that includes only non‑sensitive attributes
        attr_dict = {
            k: v for k, v in emp.__dict__.items()
            if k not in sensitive_fields
        }
        # Allow the template to reference the employee as a whole:
        context = {"employee": attr_dict}

        try:
            formatted = dir_template.format(**context)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to format entry for {emp.name}: {exc}") from exc

        entries.append(formatted)

    return "\n".join(entries)