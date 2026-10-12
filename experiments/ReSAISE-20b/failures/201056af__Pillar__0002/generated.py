import re
from typing import List

# ----------------------------------------------------------------------
# Sample data model (would normally come from a database or other source)
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example dataset – in real use this would be replaced by actual data
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@example.com"),
    Employee("Carol Williams", "Analyst", "Finance", 70000, "carol@example.com"),
]

# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        Department name to filter employees.
    list_template : str
        String template containing placeholders such as '{employee.name}'.

    Returns
    -------
    str
        The concatenated formatted string for all employees in the department.

    Raises
    ------
    ValueError
        If restricted fields are accessed or an unexpected error occurs.
    """
    # Allowed placeholder attributes
    allowed_attrs = {"name", "position"}

    # Regex to find all placeholders of the form {employee.<attr>}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")

    # Find all unique placeholders in the template
    placeholders = set(placeholder_pattern.findall(list_template))

    # Validate placeholders – disallow restricted fields
    for attr in placeholders:
        if attr not in allowed_attrs:
            raise ValueError(f"Access to restricted field '{attr}' is forbidden")

    # Filter employees by department
    relevant_employees = [e for e in EMPLOYEES if e.department == team_name]

    # Build the result string
    lines = []
    try:
        for emp in relevant_employees:
            # Create a mapping for formatting
            context = {f"employee.{attr}": getattr(emp, attr) for attr in allowed_attrs}
            line = list_template.format(**context)
            lines.append(line)
    except Exception as exc:
        # Any unexpected exception is wrapped in ValueError
        raise ValueError(f"Failed to build worker list: {exc}") from exc

    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(build_worker_list("Engineering", tmpl))