import re
from types import SimpleNamespace
from dataclasses import dataclass
from typing import List

# ----------------------------------------------------------------------
# Example Employee class – in a real system this would be imported
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float          # sensitive – must not be exposed
    personal_email: str    # sensitive – must not be exposed

# ----------------------------------------------------------------------
# Sample data – replace with real employee list in production
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000, "bob.johnson@example.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 68000, "carol.lee@example.com"),
]

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted directory of employees belonging to the specified
    department.

    Parameters
    ----------
    team : str
        Department name.
    template_str : str
        Template containing placeholders like `{employee.name}` or
        `{employee.position}`.

    Returns
    -------
    str
        Multi‑line string with each employee formatted according to the
        template.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data (salary or
        personal_email) or if formatting fails.
    """
    # Detect any attempt to use sensitive fields
    placeholders = re.findall(r"\{([^\}]+)\}", template_str)
    for placeholder in placeholders:
        if "." not in placeholder:
            continue
        _, attr = placeholder.split(".", 1)
        if attr in {"salary", "personal_email"}:
            raise ValueError("Access to sensitive data is prohibited")

    # Build the directory
    lines = []
    for emp in EMPLOYEES:
        if getattr(emp, "department", None) != team:
            continue

        # Use SimpleNamespace to expose attributes as dot‑accessible
        employee_obj = SimpleNamespace(
            name=emp.name,
            position=emp.position,
        )

        try:
            formatted = template_str.format(employee=employee_obj)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Template formatting error: {exc}") from exc

        lines.append(formatted)

    return "\n".join(lines)