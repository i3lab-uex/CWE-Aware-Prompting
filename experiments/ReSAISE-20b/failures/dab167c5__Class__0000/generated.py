import re
from typing import List

# Assuming an Employee class and a global list of employees exist in the context.
# If they are not defined, import them from the appropriate module or define stubs for testing.
try:
    from employee_module import Employee, EMPLOYEES  # Replace with the actual module name
except Exception:
    # Minimal stub for demonstration/testing purposes
    class Employee:
        def __init__(self, name: str, position: str, department: str,
                     salary: float = 0.0, personal_email: str = ""):
            self.name = name
            self.position = position
            self.department = department
            self.salary = salary
            self.personal_email = personal_email

    EMPLOYEES: List[Employee] = []

def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Args:
        team: Department name to filter employees.
        template_str: Template string containing placeholders like
                      '{employee.name}' or '{employee.position}'.

    Returns:
        A string containing each employee's details formatted according to
        the template, separated by newlines.

    Raises:
        ValueError: If sensitive fields (salary or personal_email) are requested
                    or if any other error occurs during processing.
    """
    # Detect disallowed placeholders before processing
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    disallowed_fields = {"salary", "personal_email"}

    for match in placeholder_pattern.finditer(template_str):
        field_name = match.group(1).strip()
        if field_name in disallowed_fields:
            raise ValueError(f"Access to sensitive data '{field_name}' is prohibited.")

    # Filter employees by department
    filtered_employees = [e for e in EMPLOYEES if e.department.lower() == team.lower()]

    # Prepare formatted lines
    lines = []
    for employee in filtered_employees:
        try:
            # Use a safe replacement strategy
            def repl(m):
                field = m.group(1).strip()
                return str(getattr(employee, field))
            formatted_line = placeholder_pattern.sub(repl, template_str)
            lines.append(formatted_line)
        except Exception as exc:
            raise ValueError(f"Failed to format employee data: {exc}") from exc

    return "\n".join(lines)