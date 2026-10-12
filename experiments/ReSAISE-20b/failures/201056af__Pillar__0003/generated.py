import re
from typing import List

# ----------------------------------------------------------------------
# Dummy data structures for illustration. In a real application these
# would come from a database or another persistent storage layer.
# ----------------------------------------------------------------------
class Employee:
    """Represents an employee with a few attributes."""
    def __init__(self, name: str, position: str,
                 department: str, salary: float,
                 personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example global employee list. In production this would be injected or
# retrieved from a repository.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob.johnson@company.com"),
    Employee("Carol White", "Analyst", "Finance", 75000, "carol.white@company.com"),
]

# ----------------------------------------------------------------------
# Core implementation
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "position", "department"}
RESTRICTED_FIELDS = {"salary", "personal_email"}

PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        Department name to filter employees by.
    list_template : str
        A template string containing placeholders like
        `{employee.name}` or `{employee.position}`.

    Returns
    -------
    str
        A string with each employee's information inserted into the
        template, one per line.

    Raises
    ------
    ValueError
        If the template references a restricted field or an unknown
        attribute, or if any other unexpected error occurs.
    """
    try:
        # Filter employees by department (case-insensitive match)
        team_employees = [
            emp for emp in EMPLOYEES if emp.department.lower() == team_name.lower()
        ]

        if not team_employees:
            return f"No employees found in department '{team_name}'."

        # Validate template placeholders
        for match in PLACEHOLDER_RE.finditer(list_template):
            field = match.group(1)
            if field in RESTRICTED_FIELDS:
                raise ValueError(f"Access to restricted field '{field}' is not allowed.")
            if field not in ALLOWED_FIELDS:
                raise ValueError(f"Unknown placeholder '{field}' in template.")

        # Build the output
        lines = []
        for emp in team_employees:
            def repl(match):
                field_name = match.group(1)
                return str(getattr(emp, field_name))

            line = PLACEHOLDER_RE.sub(repl, list_template)
            lines.append(line)

        return "\n".join(lines)

    except ValueError:
        # Propagate ValueErrors explicitly
        raise
    except Exception as exc:  # pragma: no cover
        # Wrap any other exception in a ValueError for consistency
        raise ValueError(f"An unexpected error occurred: {exc}") from exc

# ----------------------------------------------------------------------
# Example usage (for manual testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(build_worker_list("Engineering", template))