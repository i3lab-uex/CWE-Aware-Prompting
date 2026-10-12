import re
from typing import List

# --------------------------------------------------------------------------- #
# Mocked context – in the real system these would be provided by the
# application.  They are included here only so that the module can be run
# independently for testing purposes.
# --------------------------------------------------------------------------- #
class Employee:
    """
    Simple employee data holder.  In the real application this would be
    a fully‑fledged ORM model or a dataclass.
    """
    __slots__ = ("name", "position", "department",
                 "salary", "personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

def get_all_employees() -> List[Employee]:
    """
    Return a list of all employees.  Replace this with the real data
    source in production.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 90000.0,
                 "alice.smith@company.com"),
        Employee("Bob Johnson", "Senior Engineer", "Engineering",
                 120000.0, "bob.johnson@company.com"),
        Employee("Carol Williams", "HR Manager", "Human Resources",
                 95000.0, "carol.williams@company.com"),
    ]

# --------------------------------------------------------------------------- #
# Implementation of the required function
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {"name", "position", "department"}

PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department.

    Parameters
    ----------
    department : str
        The name of the department whose employees should be listed.
    template : str
        A string containing placeholders such as '{employee.name}'
        or '{employee.position}'.  Each placeholder will be replaced
        with the corresponding attribute of an employee.

    Returns
    -------
    str
        A multiline string containing a formatted line for each
        employee in the specified department.

    Raises
    ------
    ValueError
        If the template contains a placeholder that references an
        attribute other than ``name``, ``position`` or ``department``,
        or if any other unexpected error occurs during processing.
    """
    # Validate template placeholders first
    for match in PLACEHOLDER_RE.finditer(template):
        field = match.group(1)
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to sensitive or unsupported attribute "
                f"'employee.{field}' is not allowed."
            )

    # Build the directory
    lines = []
    for emp in get_all_employees():
        if emp.department != department:
            continue
        # Replace placeholders safely using a dictionary of allowed fields
        values = {field: getattr(emp, field) for field in ALLOWED_FIELDS}
        try:
            line = template.format(employee=values)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to format line for employee "
                             f"{emp.name!r}: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    dept = "Engineering"
    tmpl = "{employee.name} - {employee.position}"
    print(create_employee_directory(dept, tmpl))