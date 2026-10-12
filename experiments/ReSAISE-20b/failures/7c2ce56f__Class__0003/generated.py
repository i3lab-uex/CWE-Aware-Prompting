import re
from typing import List

# ----------------------------------------------------------------------
# Employee model (for illustration only)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# In-memory employee database (replace with real persistence in production)
# ----------------------------------------------------------------------
EMPLOYEE_DB: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@corp.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000.0, "bob.johnson@corp.com"),
    Employee("Carol White", "HR Specialist", "Human Resources", 65000.0, "carol.white@corp.com"),
    # Add more employees as needed
]

# ----------------------------------------------------------------------
# Helper: Render a single employee against the template
# ----------------------------------------------------------------------
def _render_employee(template: str, employee: Employee) -> str:
    """
    Render the template for a single employee.

    Raises ValueError if the template contains disallowed placeholders.
    """
    # Identify all placeholder names inside braces
    placeholders = set(re.findall(r"{([^{}]+)}", template))

    # Disallowed attributes
    disallowed = {"salary", "personal_email"}

    if placeholders & disallowed:
        raise ValueError(f"Template contains sensitive placeholder(s): {placeholders & disallowed}")

    # Build a mapping for allowed attributes
    allowed_attrs = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department
    }

    # Replace placeholders with actual values
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in allowed_attrs:
            raise ValueError(f"Unknown placeholder: {key}")
        return str(allowed_attrs[key])

    try:
        rendered = re.sub(r"{([^{}]+)}", repl, template)
    except Exception as exc:
        raise ValueError(f"Failed to render employee {employee.name}: {exc}") from exc

    return rendered


# ----------------------------------------------------------------------
# Main function: build_team_directory
# ----------------------------------------------------------------------
def build_team_directory(team: str, template_text: str) -> str:
    """
    Generate a formatted directory for all employees in the specified department.

    Parameters
    ----------
    team : str
        The name of the department to filter employees by.
    template_text : str
        A string containing placeholders such as '{employee.name}' or
        '{employee.position}'.  Only 'name', 'position', and 'department'
        are allowed; accessing 'salary' or 'personal_email' will raise
        ValueError.

    Returns
    -------
    str
        The concatenated directory entries, each rendered from the template.

    Raises
    ------
    ValueError
        If a sensitive placeholder is used or any rendering error occurs.
    """
    if not isinstance(team, str) or not team.strip():
        raise ValueError("Team must be a non-empty string")

    if not isinstance(template_text, str) or not template_text.strip():
        raise ValueError("Template text must be a non-empty string")

    # Filter employees by department (case-insensitive match)
    matching = [e for e in EMPLOYEE_DB if e.department.lower() == team.strip().lower()]
    if not matching:
        return f"No employees found in department '{team}'."

    # Render each employee and join with newlines
    rendered_entries = []
    for emp in matching:
        rendered_entries.append(_render_employee(template_text, emp))

    return "\n".join(rendered_entries)


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", tmpl))