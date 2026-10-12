import re
from typing import List

# ------------------------------------------------------------
# Mock Employee class and dataset (replace with real implementation)
# ------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example dataset – in real usage this would come from a database or API
EMPLOYEES: List[Employee] = [
    Employee("Alice Johnson", "Engineer", "Engineering", 95000, "alice@example.com"),
    Employee("Bob Smith",     "Manager",   "Engineering", 115000, "bob@example.com"),
    Employee("Carol Lee",     "Analyst",   "Finance",     78000, "carol@example.com"),
    # ... more employees ...
]

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a directory listing for all employees in `dept_name` using
    `format_template`. The template may contain placeholders of the form
    `{employee.field}` where *field* is a public attribute of Employee.

    Sensitive attributes (`salary`, `personal_email`) are disallowed. If the
    template references any of them, or if a placeholder cannot be resolved,
    a ValueError is raised.

    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    format_template : str
        Template string with placeholders like `{employee.name}`.

    Returns
    -------
    str
        A newline‑separated string with each employee formatted according to
        the template.

    Raises
    ------
    ValueError
        If a sensitive field is referenced, or if placeholder resolution fails.
    """
    # ------------------------------------------------------------
    # 1. Validate template for disallowed fields
    # ------------------------------------------------------------
    disallowed_fields = {"salary", "personal_email"}
    placeholder_pattern = r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    placeholders = re.findall(placeholder_pattern, format_template)

    for field in placeholders:
        if field in disallowed_fields:
            raise ValueError(f"Access to sensitive field '{field}' is prohibited.")

    # ------------------------------------------------------------
    # 2. Filter employees by department
    # ------------------------------------------------------------
    relevant_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    # ------------------------------------------------------------
    # 3. Format each employee
    # ------------------------------------------------------------
    formatted_lines = []
    for emp in relevant_employees:
        try:
            line = format_template.format(employee=emp)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder in template: {exc}") from exc
        formatted_lines.append(line)

    # ------------------------------------------------------------
    # 4. Join lines into final string
    # ------------------------------------------------------------
    return "\n".join(formatted_lines)

# ------------------------------------------------------------
# Example usage (commented out – remove for production)
# ------------------------------------------------------------
# if __name__ == "__main__":
#     template = "{employee.name} - {employee.position}"
#     print(build_team_directory("Engineering", template))