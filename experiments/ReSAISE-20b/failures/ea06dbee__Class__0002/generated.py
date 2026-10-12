import re
from typing import List

# Assume the Employee class is defined elsewhere in the code base.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example data – in a real system this would come from a database or other source.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Developer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 70000, "carol@company.com"),
]


def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    dep : str
        The target department.
    format_template : str
        Template containing placeholders like '{employee.name}' or
        '{employee.position}'.  Placeholders for sensitive fields (salary,
        personal_email) are prohibited.

    Returns
    -------
    str
        Concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If a sensitive field is requested or if placeholder resolution fails.
    """
    # Compile regex to find placeholders of the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Check for prohibited fields in the template
    if placeholder_pattern.search(format_template):
        for match in placeholder_pattern.finditer(format_template):
            field_name = match.group(1)
            if field_name in {"salary", "personal_email"}:
                raise ValueError(
                    f"Access to sensitive field '{field_name}' is not allowed."
                )

    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dep]
    if not dept_employees:
        return f"No employees found in department '{dep}'."

    # Build the directory string
    lines = []
    for emp in dept_employees:
        def replace_placeholder(match):
            field = match.group(1)
            if not hasattr(emp, field):
                raise ValueError(f"Employee has no attribute '{field}'.")
            return str(getattr(emp, field))

        try:
            line = placeholder_pattern.sub(replace_placeholder, format_template)
        except Exception as exc:
            raise ValueError(f"Failed to format employee data: {exc}") from exc

        lines.append(line)

    return "\n".join(lines)


# Example usage:
if __name__ == "__main__":
    template = "{employee.name} - {employee.position}"
    print(generate_staff_listing("Engineering", template))