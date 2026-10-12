import re
from typing import List

# ------------------------------
# Simple Employee model
# ------------------------------
class Employee:
    """
    Represents an employee with several attributes.
    Only name, position and department are considered safe for display.
    """
    __slots__ = ("name", "position", "department", "_salary", "_personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self._salary = salary          # internal, should not be exposed
        self._personal_email = personal_email  # internal, should not be exposed

    @property
    def salary(self):
        """Access to salary is intentionally blocked for display."""
        raise AttributeError("salary is not accessible")

    @property
    def personal_email(self):
        """Access to personal email is intentionally blocked for display."""
        raise AttributeError("personal_email is not accessible")

# ------------------------------
# Core function
# ------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A string containing placeholders in the form `{employee.<field>}`.
        Allowed fields: name, position, department.

    Returns
    -------
    str
        The populated template with employee data substituted.

    Raises
    ------
    ValueError
        If restricted fields are referenced or an unexpected error occurs.
    """
    # Example data source – in a real system this would come from DB or API
    _EMPLOYEES: List[Employee] = [
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@corp.com"),
        Employee("Bob Jones", "Manager", "Engineering", 120000, "bob.jones@corp.com"),
        Employee("Carol White", "HR Specialist", "Human Resources", 70000, "carol.white@corp.com"),
    ]

    # Define which fields are allowed to be exposed
    SAFE_FIELDS = {"name", "position", "department"}

    # Regex to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Find all unique placeholders in the template
    placeholders = set(placeholder_pattern.findall(list_template))

    # Validate placeholders – disallow restricted fields
    for field in placeholders:
        if field not in SAFE_FIELDS:
            raise ValueError(f"Access to restricted or unknown employee field '{field}' is prohibited.")

    # Filter employees by department
    filtered = [emp for emp in _EMPLOYEES if emp.department == team_name]
    if not filtered:
        return f"No employees found in department '{team_name}'."

    # Build the output string
    output_parts = []
    for emp in filtered:
        try:
            # Create a mapping from placeholder to actual value
            values = {f"employee.{field}": getattr(emp, field) for field in placeholders}
            # Perform substitution
            formatted = list_template.format(**values)
        except Exception as exc:
            raise ValueError(f"Failed to format employee data: {exc}") from exc
        output_parts.append(formatted)

    return "\n".join(output_parts)