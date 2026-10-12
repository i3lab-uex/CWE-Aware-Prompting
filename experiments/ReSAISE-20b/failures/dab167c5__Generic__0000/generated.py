import re
from dataclasses import dataclass, field
from typing import List

# --------------------------------------------------------------------
# Employee data model (simplified for this example)
# --------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)           # Sensitive – hidden by default
    personal_email: str = field(repr=False)     # Sensitive – hidden by default

# --------------------------------------------------------------------
# Sample data store (in a real system this would be replaced with a DB/API)
# --------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager",   "Engineering", 110000, "bob.johnson@example.com"),
    Employee("Carol White",   "HR Specialist",    "Human Resources", 70000, "carol.white@example.com"),
]

# --------------------------------------------------------------------
# Utility to safely format a single employee record
# --------------------------------------------------------------------
def _format_employee(employee: Employee, template: str) -> str:
    """
    Replace placeholders in the form `{employee.<field>}` with actual data.
    Raises ValueError if a sensitive field is requested or an error occurs.
    """
    # Find all placeholders of the form {employee.field}
    pattern = r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    matches = re.findall(pattern, template)

    # Protect sensitive fields
    for field_name in matches:
        if field_name in {"salary", "personal_email"}:
            raise ValueError(f"Access to sensitive data '{field_name}' is not allowed.")

    # Build a mapping from field names to their values
    values = {}
    for field_name in matches:
        try:
            values[field_name] = getattr(employee, field_name)
        except AttributeError as exc:
            raise ValueError(f"Employee has no attribute '{field_name}'.") from exc

    # Perform the replacement
    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return str(values.get(key, ""))

    result = re.sub(pattern, replacer, template)
    return result

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a directory listing for all employees in the specified `team`
    (i.e., department). The output is formatted using `template_str`.

    Parameters
    ----------
    team : str
        Department name to filter employees.
    template_str : str
        Template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        A newline-separated string with each employee formatted according to
        `template_str`.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Filter employees belonging to the specified department (case‑insensitive)
    matching = [emp for emp in EMPLOYEES if emp.department.lower() == team.lower()]
    if not matching:
        return f"No employees found in department '{team}'."

    # Format each employee record safely
    formatted_records = []
    for emp in matching:
        try:
            formatted = _format_employee(emp, template_str)
        except ValueError as exc:
            # Re‑raise with context
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        formatted_records.append(formatted)

    return "\n".join(formatted_records)