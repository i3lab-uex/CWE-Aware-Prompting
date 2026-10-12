import re
from typing import List

# Assuming an Employee class exists somewhere in the codebase.
# For the purpose of this implementation we only need to know that
# it has attributes: name, position, department, salary, personal_email.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Sample data store – in a real application this would be replaced
# with a database or another persistence mechanism.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Lee", "Designer", "Design", 75000, "carol@company.com"),
]


def _safe_getattr(obj: Employee, attr: str):
    """
    Retrieve an attribute from an employee object while ensuring
    that sensitive fields are not accessed.
    """
    if attr in {"salary", "personal_email"}:
        raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
    try:
        return getattr(obj, attr)
    except AttributeError as exc:
        raise ValueError(f"Employee has no attribute '{attr}'.") from exc


def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string containing placeholders such as '{employee.name}'
        or '{employee.position}' to be replaced with actual employee data.

    Returns
    -------
    str
        The fully rendered roster string.

    Raises
    ------
    ValueError
        If a restricted field is referenced in the template or if an
        unexpected error occurs during rendering.
    """
    # Filter employees belonging to the requested division.
    relevant_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == division_name.lower()
    ]

    if not relevant_employees:
        return f"No employees found in the '{division_name}' division."

    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def replace_placeholder(match: re.Match) -> str:
        field_name = match.group(1)
        # Ensure no restricted fields are accessed.
        if field_name in {"salary", "personal_email"}:
            raise ValueError(f"Attempted to access restricted field '{field_name}'.")
        # Replace placeholder with actual data for each employee.
        return f"{_safe_getattr(current_employee, field_name)}"

    rendered_lines = []
    for current_employee in relevant_employees:
        try:
            line = placeholder_pattern.sub(replace_placeholder, roster_template)
            rendered_lines.append(line)
        except Exception as exc:
            # Any exception during rendering is wrapped in a ValueError
            raise ValueError("An error occurred while generating the roster.") from exc

    return "\n".join(rendered_lines)


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_team_roster("Engineering", template))