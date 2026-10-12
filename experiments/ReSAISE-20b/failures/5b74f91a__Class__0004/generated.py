import re
from typing import List

# ------------------------------------------------------------------
# Dummy Employee class and sample data (in a real system this would
# be imported from your application package)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Sample data for demonstration purposes.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 115000.0, "bob.johnson@example.com"),
    Employee("Carol White", "Analyst", "Finance", 72000.0, "carol.white@example.com"),
]

# ------------------------------------------------------------------
# Build team directory function
# ------------------------------------------------------------------
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Args:
        dept_name: Name of the department to filter employees.
        format_template: Template string containing placeholders such as
                         '{employee.name}', '{employee.position}'.

    Returns:
        A string containing the formatted directory entries, one per line.

    Raises:
        ValueError: If the template tries to access sensitive fields
                    (salary or personal_email) or if any other error occurs.
    """
    # Define fields that are considered sensitive
    SENSITIVE_FIELDS = {"salary", "personal_email"}

    # Compile a regex that finds placeholders like {employee.field}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

    # Verify that no sensitive field is requested
    for match in placeholder_pattern.finditer(format_template):
        field_name = match.group(1)
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is not allowed.")

    # Filter employees belonging to the specified department
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not dept_employees:
        return f"No employees found in department '{dept_name}'."

    # Build the directory lines
    lines = []
    for employee in dept_employees:
        try:
            # Create a mapping that the template can use
            mapping = {"employee": employee}
            line = format_template.format(**mapping)
        except Exception as exc:
            raise ValueError(f"Failed to format employee '{employee.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)