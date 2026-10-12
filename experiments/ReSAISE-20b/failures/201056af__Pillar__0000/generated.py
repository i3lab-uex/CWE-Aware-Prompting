import re
from typing import List

# ------------------------------------------------------------------
# Example Employee class (for illustration; in real usage this would
# come from your application).  Only the public attributes are used.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# A global registry of employees.  In a real application this might
# be replaced by a database query or another data source.
# ------------------------------------------------------------------
EMPLOYEE_REGISTRY: List[Employee] = []

# ------------------------------------------------------------------
# Allowed fields that may appear in the template.  Anything else
# (e.g., salary, personal_email) is considered restricted.
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "position"}

_PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference restricted fields.
    Raises ValueError if a forbidden field is found.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        field = match.group(1)
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Template references restricted or unknown field: '{field}'"
            )

def _render_employee(employee: Employee, template: str) -> str:
    """
    Render a single employee's data into the provided template.
    Raises ValueError if any placeholder cannot be resolved.
    """
    def repl(match: re.Match) -> str:
        field = match.group(1)
        try:
            value = getattr(employee, field)
        except AttributeError as exc:
            raise ValueError(f"Employee has no attribute '{field}'") from exc
        return str(value)

    try:
        rendered = _PLACEHOLDER_RE.sub(repl, template)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Unexpected error during template rendering") from exc

    return rendered

def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A string containing placeholders like `{employee.name}` or
        `{employee.position}`.  The template may be repeated for each
        employee; the function will concatenate the results.

    Returns
    -------
    str
        A single string containing the rendered information for all
        employees in the specified department.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary,
        personal_email) or any other unexpected error occurs.
    """
    if not isinstance(team_name, str):
        raise ValueError("team_name must be a string")
    if not isinstance(list_template, str):
        raise ValueError("list_template must be a string")

    # Validate the template once
    _validate_template(list_template)

    # Filter employees by department
    matching_employees = [
        emp for emp in EMPLOYEE_REGISTRY if emp.department == team_name
    ]

    # Render each employee's information
    rendered_lines = []
    for emp in matching_employees:
        rendered_line = _render_employee(emp, list_template)
        rendered_lines.append(rendered_line)

    # Join with newlines (or any separator you prefer)
    return "\n".join(rendered_lines)

# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the registry with some sample data
    EMPLOYEE_REGISTRY.extend([
        Employee("Alice", "Engineer", "Engineering", 90000, "alice@corp.com"),
        Employee("Bob", "Designer", "Design", 80000, "bob@corp.com"),
        Employee("Charlie", "Engineer", "Engineering", 95000, "charlie@corp.com"),
    ])

    template = "- {employee.name} ({employee.position})"
    try:
        print(build_worker_list("Engineering", template))
    except ValueError as e:
        print(f"Error: {e}")