import re
from typing import List

# ----------------------------------------------------------------------
# Dummy Employee model – replace with your actual implementation.
# ----------------------------------------------------------------------
class Employee:
    """Simple representation of an employee."""
    def __init__(self, name: str, position: str,
                 department: str, salary: float,
                 personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# Sample data – replace with your actual employee repository.
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 70000, "carol@company.com"),
]

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_team_roster(division_name: str, roster_template: str) -> str:
    """
    Generates a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The department name to filter employees by.
    roster_template : str
        A string template containing placeholders such as `{employee.name}` or
        `{employee.position}`.

    Returns
    -------
    str
        The formatted directory string, one employee per line.

    Raises
    ------
    ValueError
        If the template references restricted attributes (salary, personal_email)
        or if an unexpected error occurs during formatting.
    """
    # Allowed attributes for security reasons
    SAFE_ATTRIBUTES = {"name", "position", "department"}

    # ------------------------------------------------------------------
    # Validate template placeholders
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    placeholders = set(placeholder_pattern.findall(roster_template))

    # Check for disallowed attributes
    restricted = {"salary", "personal_email"}
    if any(attr in restricted for attr in placeholders):
        raise ValueError(
            f"Template contains restricted attribute(s): "
            f"{', '.join(sorted(restricted & placeholders))}"
        )

    # Ensure all placeholders are allowed
    if not placeholders.issubset(SAFE_ATTRIBUTES):
        unknown = placeholders - SAFE_ATTRIBUTES
        raise ValueError(
            f"Template contains unknown attribute(s): {', '.join(sorted(unknown))}"
        )

    # ------------------------------------------------------------------
    # Filter employees by department
    # ------------------------------------------------------------------
    try:
        dept_employees = [
            emp for emp in EMPLOYEES if emp.department.lower() == division_name.lower()
        ]
    except Exception as exc:
        raise ValueError(f"Failed to filter employees: {exc}") from exc

    # ------------------------------------------------------------------
    # Format each employee
    # ------------------------------------------------------------------
    lines = []
    for emp in dept_employees:
        try:
            # Build a mapping for the template
            context = {"employee": emp}
            line = roster_template.format_map(context)
            lines.append(line)
        except KeyError as ke:
            raise ValueError(f"Missing key in template: {ke}") from ke
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc

    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage (commented out – remove to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    try:
        output = generate_team_roster("Engineering", template)
        print(output)
    except ValueError as err:
        print(f"Error: {err}")