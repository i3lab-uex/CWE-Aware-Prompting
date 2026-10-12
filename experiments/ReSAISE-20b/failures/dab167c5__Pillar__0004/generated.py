import re
from dataclasses import dataclass
from typing import List

# ----------------------------------------------------------------------
# Sample Employee definition (would normally be provided elsewhere)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# ----------------------------------------------------------------------
# Example data store (would normally be populated elsewhere)
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Developer", "Engineering", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Designer", "Design", 85000.0, "bob.johnson@company.com"),
    Employee("Carol Williams", "Manager", "Engineering", 120000.0, "carol.williams@company.com"),
    # ... more employees ...
]

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_team_roster(team: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    team : str
        The name of the department whose employees should be listed.
    template_str : str
        A string containing placeholders in the form {employee.<field>}.
        Only non‑sensitive fields are allowed.

    Returns
    -------
    str
        The concatenated formatted string for all employees in the team.

    Raises
    ------
    ValueError
        If a placeholder references sensitive data (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Compile a regex to find placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

    # Identify all placeholders used in the template
    fields_in_template = set(match.group(1) for match in placeholder_pattern.finditer(template_str))

    # Disallow sensitive fields
    forbidden = {"salary", "personal_email"}
    if forbidden & fields_in_template:
        raise ValueError(f"Access to sensitive data is not permitted: {forbidden & fields_in_template}")

    # Ensure all requested fields exist on Employee
    employee_fields = {f.name for f in dataclass.fields(Employee)}
    unknown_fields = fields_in_template - employee_fields
    if unknown_fields:
        raise ValueError(f"Unknown employee attribute(s) in template: {unknown_fields}")

    # Filter employees belonging to the specified team (case‑insensitive)
    selected_employees = [e for e in EMPLOYEES if e.department.lower() == team.lower()]

    # If no employees found, return an empty string
    if not selected_employees:
        return ""

    # Helper function to format a single employee
    def _format_employee(emp: Employee) -> str:
        # Build a mapping for formatting
        context = {f"employee.{field}": getattr(emp, field) for field in fields_in_template}
        try:
            return template_str.format(**context)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Formatting error for employee {emp.name}: {exc}") from exc

    # Format each employee and join with newlines
    formatted_lines = [_format_employee(emp) for emp in selected_employees]
    return "\n".join(formatted_lines)

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_team_roster("Engineering", tmpl))