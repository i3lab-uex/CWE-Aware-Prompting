import string
from typing import List

# ------------------------------------------------------------------
# Employee model (simplified for this example)
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
# Mock data source – in a real application this would query a DB
# ------------------------------------------------------------------
def get_all_employees() -> List[Employee]:
    """Return all employees in the organization."""
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
        Employee("Bob Jones",   "Manager",  "Engineering", 120000, "bob@company.com"),
        Employee("Carol Lee",   "Analyst",  "Finance",     75000,  "carol@company.com"),
    ]

# ------------------------------------------------------------------
# Utility: find all placeholder fields in a template
# ------------------------------------------------------------------
def _extract_placeholder_fields(template: str) -> List[str]:
    """Return a list of placeholder field names found in the template."""
    formatter = string.Formatter()
    fields = []
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:
            fields.append(field_name)
    return fields

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A string template containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The concatenated formatted entries for each employee in the department.

    Raises
    ------
    ValueError
        If the template attempts to access restricted fields (salary or personal_email)
        or if any unexpected error occurs during formatting.
    """
    # Define restricted fields that should never be exposed
    RESTRICTED = {"employee.salary", "employee.personal_email"}

    # Validate template for restricted fields
    placeholders = _extract_placeholder_fields(list_template)
    for ph in placeholders:
        if ph in RESTRICTED:
            raise ValueError(f"Access to restricted field '{ph}' is not allowed.")

    # Filter employees by department
    all_emps = get_all_employees()
    team_emps = [emp for emp in all_emps if emp.department == team_name]

    # Prepare the output
    lines = []
    for emp in team_emps:
        try:
            # Build a context dict mapping 'employee.<attr>' to the actual value
            context = {f"employee.{attr}": getattr(emp, attr)
                       for attr in vars(emp).keys()
                       if not attr.startswith("_")}
            line = list_template.format(**context)
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)