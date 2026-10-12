import re
from dataclasses import dataclass, fields
from typing import List

# ------------------------------------------------------------------
# Employee definition (normally this would be imported from the app)
# ------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# ------------------------------------------------------------------
# Sample data store – in a real application this would be replaced
# by a database query or other persistence layer.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Developer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Designer", "Engineering", 85000, "bob.johnson@example.com"),
    Employee("Carol White", "Manager", "HR", 105000, "carol.white@example.com"),
    # ... more employees ...
]

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
_SENSITIVE_FIELDS = {"salary", "personal_email"}

def _is_sensitive(field_name: str) -> bool:
    """Return True if the field is considered sensitive."""
    return field_name.lower() in _SENSITIVE_FIELDS

def _safe_getattr(obj, attr: str):
    """Get attribute value if it is not sensitive; otherwise raise ValueError."""
    if _is_sensitive(attr):
        raise ValueError(f"Attempt to access sensitive field '{attr}'.")
    if not hasattr(obj, attr):
        raise ValueError(f"Employee has no attribute '{attr}'.")
    return getattr(obj, attr)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_team_directory(team: str, template_text: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        Department name used to filter employees.
    template_text : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The directory with each employee's details formatted according to the template.

    Raises
    ------
    ValueError
        If a placeholder refers to a sensitive field, an unknown attribute,
        or if any other error occurs during processing.
    """
    # Filter employees by department (case‑insensitive match)
    selected = [e for e in EMPLOYEES if e.department.lower() == team.lower()]
    if not selected:
        return ""  # No employees in this department

    # Regex to find placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Build the directory
    lines = []
    for emp in selected:
        def replace(match):
            field_name = match.group(1)
            try:
                value = _safe_getattr(emp, field_name)
            except ValueError as exc:
                raise ValueError(f"Error processing employee '{emp.name}': {exc}") from None
            return str(value)

        try:
            formatted = placeholder_pattern.sub(replace, template_text)
        except ValueError as exc:
            # Propagate the error with context
            raise ValueError(f"Failed to format entry for '{emp.name}': {exc}") from None

        lines.append(formatted)

    return "\n".join(lines)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", tmpl))