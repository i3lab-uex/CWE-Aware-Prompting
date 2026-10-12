import re
from typing import List

# ----------------------------------------------------------------------
# Dummy Employee class and sample data (replace with real implementation)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example employee list – in real usage this would come from a database or
# another data source.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "DevOps Engineer",   "Engineering", 88000.0, "bob.johnson@example.com"),
    Employee("Carol White",   "HR Manager",      "Human Resources", 72000.0, "carol.white@example.com"),
    # ... more employees ...
]

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory string for all employees in the given department.

    Parameters
    ----------
    dept_name : str
        Name of the department to filter employees by.
    format_template : str
        Template string containing placeholders like `{employee.name}` or
        `{employee.position}`. The template must not reference sensitive fields
        (`salary`, `personal_email`).

    Returns
    -------
    str
        The formatted directory, each employee on a separate line.

    Raises
    ------
    ValueError
        If the template contains forbidden placeholders, or if a placeholder
        refers to an attribute that does not exist.
    """
    # Compile regex for placeholders: {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Detect forbidden placeholders
    for match in placeholder_pattern.finditer(format_template):
        field = match.group(1)
        if field in {"salary", "personal_email"}:
            raise ValueError(f"Access to sensitive data '{field}' is forbidden in the template.")

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dept_name]

    # Prepare the formatted lines
    lines = []
    for emp in dept_employees:
        try:
            line = placeholder_pattern.sub(lambda m: str(getattr(emp, m.group(1))), format_template)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder in template: {exc}") from None
        lines.append(line)

    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(build_team_directory("Engineering", template))