import re
from typing import List

# ----------------------------------------------------------------------
# Minimal Employee model used for the example.
# In a real project this would come from an external module or database.
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# Example data source – in practice this would be replaced by a
# database query or an API call.
# ----------------------------------------------------------------------
def _get_all_employees() -> List[Employee]:
    """
    Return a list of all employees.  In production this would be
    replaced by a proper data source.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 90000.0, "alice@company.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob@company.com"),
        Employee("Carol Lee",   "Analyst",  "Finance",    75000.0, "carol@company.com"),
        # ... more employees ...
    ]

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted string listing all employees that belong to
    *team_name* by replacing placeholders in *list_template*.

    The template may contain placeholders of the form `{employee.<field>}`.
    Only `name`, `position` and `department` are allowed.  Attempts to
    access restricted fields such as `salary` or `personal_email`
    raise a :class:`ValueError`.

    Parameters
    ----------
    team_name : str
        The department name to filter employees by.
    list_template : str
        A template string containing placeholders for employee data.

    Returns
    -------
    str
        The resulting directory string.

    Raises
    ------
    ValueError
        If a restricted field is requested or if any other error occurs.
    """
    # Regular expression to find placeholders like `{employee.name}`
    placeholder_re = re.compile(r"\{employee\.([a-zA-Z_]+)\}")

    # Allowed fields – anything else is considered restricted
    allowed_fields = {"name", "position", "department"}

    # Prepare a list to hold the rendered lines
    rendered_lines = []

    try:
        all_employees = _get_all_employees()
        # Filter employees by the requested department
        team_members = [e for e in all_employees if e.department == team_name]

        for employee in team_members:
            # Function to replace a single placeholder
            def repl(match: re.Match) -> str:
                field = match.group(1)
                if field not in allowed_fields:
                    raise ValueError(
                        f"Access to restricted field '{field}' is not permitted."
                    )
                return str(getattr(employee, field))

            # Apply replacements to the template
            rendered = placeholder_re.sub(repl, list_template)
            rendered_lines.append(rendered)

        return "\n".join(rendered_lines)

    except ValueError:
        # Re‑raise explicit value errors
        raise
    except Exception as exc:  # pragma: no cover
        # Wrap any other exception in a ValueError to keep the API stable
        raise ValueError(f"An unexpected error occurred: {exc}") from exc

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Employee: {employee.name}, Position: {employee.position}"
    try:
        output = build_worker_list("Engineering", tmpl)
        print(output)
    except ValueError as e:
        print(f"Error: {e}")