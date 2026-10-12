import re
from dataclasses import dataclass, fields
from typing import List

# Example Employee class – in a real project this would be imported from the relevant module.
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# A global list of employees for demonstration purposes.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000.0, "bob.johnson@example.com"),
    Employee("Carol Williams", "HR Specialist", "Human Resources", 70000.0, "carol.williams@example.com"),
    # ... more employees ...
]

# Set of fields that are considered restricted and must not appear in the template.
RESTRICTED_FIELDS = {"salary", "personal_email"}

# Regular expression to find placeholders of the form {employee.<field>}
PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any restricted fields.
    Raise ValueError if a forbidden field is found.
    """
    for match in PLACEHOLDER_RE.finditer(template):
        field_name = match.group(1)
        if field_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed in the template.")

def _render_employee(employee: Employee, template: str) -> str:
    """
    Render a single employee using the provided template.
    Any placeholder that does not correspond to an Employee attribute
    will raise a ValueError.
    """
    def repl(match):
        field_name = match.group(1)
        if not hasattr(employee, field_name):
            raise ValueError(f"Template references unknown field '{field_name}'.")
        return str(getattr(employee, field_name))
    try:
        return PLACEHOLDER_RE.sub(repl, template)
    except Exception as exc:
        raise ValueError(f"Error rendering employee data: {exc}") from exc

def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The name of the department to filter employees by.
    roster_template : str
        A string template containing placeholders like `{employee.name}` and `{employee.position}`.

    Returns
    -------
    str
        A multiline string where each line represents an employee in the department,
        formatted according to `roster_template`.

    Raises
    ------
    ValueError
        If the template references restricted fields (`salary`, `personal_email`) or any other
        unexpected error occurs during processing.
    """
    try:
        _validate_template(roster_template)

        # Filter employees by department (case‑insensitive match).
        filtered = [emp for emp in EMPLOYEES if emp.department.lower() == division_name.lower()]

        # Render each employee line.
        rendered_lines = [_render_employee(emp, roster_template) for emp in filtered]

        # Join lines with a newline separator.
        return "\n".join(rendered_lines)
    except ValueError:
        # Re‑raise any ValueErrors directly.
        raise
    except Exception as exc:
        # Wrap unexpected exceptions in a ValueError for consistency.
        raise ValueError(f"An error occurred while generating the roster: {exc}") from exc