import re
from typing import List

# Assuming the Employee class is defined elsewhere in the codebase.
# Here we provide a minimal stub for type checking and demonstration purposes.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = None, personal_email: str = None):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# Mock data source – in a real application this would come from a database or service.
_EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering",
             salary=95000, personal_email="alice@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering",
             salary=105000, personal_email="bob@example.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources",
             salary=65000, personal_email="carol@example.com"),
]


def _filter_employees_by_department(dept_name: str) -> List[Employee]:
    """Return a list of employees belonging to the given department."""
    return [e for e in _EMPLOYEES if e.department.lower() == dept_name.lower()]


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a directory string for all employees in ``dept_name`` using
    ``format_template``.

    Parameters
    ----------
    dept_name : str
        The department whose employees should be listed.
    format_template : str
        A string containing placeholders like ``{employee.name}`` or
        ``{employee.position}``.  Placeholders referring to *salary* or
        *personal_email* are considered sensitive and will cause a ValueError.

    Returns
    -------
    str
        A newline‑separated string with each employee formatted according to
        ``format_template``.

    Raises
    ------
    ValueError
        If a sensitive field is requested or if the template references an
        unknown attribute.
    """
    # Identify all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(format_template)

    # Validate placeholders
    for ph in placeholders:
        # Only allow 'employee.<field>' syntax
        if not ph.startswith("employee."):
            raise ValueError(f"Unsupported placeholder format: {{{ph}}}")

        field_name = ph.split(".", 1)[1]
        if field_name in ("salary", "personal_email"):
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

    # Gather employees for the requested department
    dept_employees = _filter_employees_by_department(dept_name)
    if not dept_employees:
        return f"No employees found in department '{dept_name}'."

    # Build the directory string
    lines = []
    for emp in dept_employees:
        try:
            line = format_template.format(employee=emp)
        except AttributeError as exc:
            # If the employee object does not have the requested attribute
            raise ValueError(f"Invalid field in template: {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", template))