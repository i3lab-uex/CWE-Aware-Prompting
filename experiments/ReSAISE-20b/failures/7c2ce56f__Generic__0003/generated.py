import re
from typing import List, Any

# Assuming an Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float  # sensitive
# personal_email: str  # sensitive
try:
    from employee import Employee  # noqa: F401
except Exception:
    # Minimal placeholder for type checking; real implementation should import the actual class.
    class Employee:  # pragma: no cover
        name: str
        position: str
        department: str
        salary: float
        personal_email: str


def build_team_directory(team: str, template_text: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Args:
        team (str): The department name used to filter employees.
        template_text (str): A string containing placeholders such as
                             '{employee.name}', '{employee.position}'.

    Returns:
        str: The directory string with placeholders replaced by employee data
             for all employees in the specified department.

    Raises:
        ValueError: If the template attempts to access sensitive attributes
                    (salary or personal_email) or if any error occurs during
                    formatting.
    """
    # Define sensitive attributes that must not be exposed
    SENSITIVE_ATTRS = {"salary", "personal_email"}

    # Detect placeholders and ensure no sensitive data is requested
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    for match in placeholder_pattern.finditer(template_text):
        expr = match.group(1).strip()
        # We only allow simple attribute access of the form 'employee.<attr>'
        if expr.startswith("employee."):
            attr = expr.split(".", 1)[1]
            if attr in SENSITIVE_ATTRS:
                raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed.")
        else:
            # If the expression does not start with 'employee.', we treat it as invalid
            raise ValueError(f"Unsupported placeholder '{expr}'. Only 'employee.<attr>' is allowed.")

    # Retrieve all employees (this would normally come from a database or service)
    try:
        all_employees: List[Employee] = _get_all_employees()
    except Exception as exc:
        raise ValueError(f"Failed to retrieve employees: {exc}") from exc

    # Filter by department
    dept_employees = [e for e in all_employees if getattr(e, "department", None) == team]

    # Format each employee entry
    formatted_entries: List[str] = []
    for emp in dept_employees:
        try:
            entry = template_text.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Error formatting entry for employee '{getattr(emp, 'name', '<unknown>')}': {exc}") from exc
        formatted_entries.append(entry)

    # Join entries with a newline separator
    return "\n".join(formatted_entries)


# --------------------------------------------------------------------------- #
# The following helper function simulates retrieving employees.
# In a real application, this would query a database or another data source.
def _get_all_employees() -> List[Employee]:
    """
    Mock function to return a list of Employee objects.
    Replace with actual data retrieval logic.
    """
    # Example mock data
    class _MockEmployee(Employee):
        def __init__(self, name, position, department, salary, personal_email):
            self.name = name
            self.position = position
            self.department = department
            self.salary = salary
            self.personal_email = personal_email

    return [
        _MockEmployee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
        _MockEmployee("Bob Johnson", "Manager", "Engineering", 115000, "bob.johnson@example.com"),
        _MockEmployee("Carol White", "Analyst", "Finance", 75000, "carol.white@example.com"),
    ]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", tmpl))