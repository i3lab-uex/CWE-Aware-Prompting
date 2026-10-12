import re
from typing import List

# ------------------------------------------------------------------
# Assume an Employee class exists in the same module or is imported
# ------------------------------------------------------------------
class Employee:
    """Simple representation of an employee."""
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary          # restricted field
        self.personal_email = personal_email  # restricted field


# ------------------------------------------------------------------
# Sample data – in real usage this would come from a database or
# other persistent store.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob@company.com"),
    Employee("Carol Lee", "Designer", "Design", 85000.0, "carol@company.com"),
    # ... more employees ...
]


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    team_name : str
        Department name to filter employees by.
    list_template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        A single string with each employee's information formatted according to
        `list_template`, separated by newlines.

    Raises
    ------
    ValueError
        If a restricted field is accessed or if an unexpected error occurs.
    """
    # Compile the placeholder regex once
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Restricted attributes that must not be exposed
    restricted_fields = {"salary", "personal_email"}

    # Filter employees by department (case‑insensitive match)
    filtered = [e for e in EMPLOYEES if e.department.lower() == team_name.lower()]
    if not filtered:
        return f"No employees found in department '{team_name}'."

    # Helper to replace placeholders for a single employee
    def _render_for_employee(emp: Employee) -> str:
        def repl(match):
            field = match.group(1)
            if field in restricted_fields:
                raise ValueError(f"Access to restricted field '{field}' is not allowed.")
            if not hasattr(emp, field):
                raise ValueError(f"Employee has no attribute '{field}'.")
            return str(getattr(emp, field))

        try:
            return placeholder_pattern.sub(repl, list_template)
        except Exception as exc:
            # Wrap any unexpected exception into ValueError
            raise ValueError(f"Failed to render template: {exc}") from exc

    # Render each employee and join with newlines
    rendered_lines = [_render_for_employee(e) for e in filtered]
    return "\n".join(rendered_lines)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "- {employee.name} ({employee.position})"
#     print(build_worker_list("Engineering", template))