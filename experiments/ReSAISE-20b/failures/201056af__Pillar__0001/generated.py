import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes:
# name: str
# position: str
# department: str
# salary: float (restricted)
# personal_email: str (restricted)

ALLOWED_FIELDS = {"name", "position", "department"}

PLACEHOLDER_PATTERN = re.compile(r"{employee\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def build_worker_list(team_name: str, list_template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    team_name : str
        The name of the department to filter employees by.
    list_template : str
        A template string containing placeholders such as
        `{employee.name}` and `{employee.position}`.

    Returns
    -------
    str
        A string containing the formatted directory, one employee per line.

    Raises
    ------
    ValueError
        If a restricted field (salary or personal_email) is referenced in the
        template, or if an unexpected error occurs during processing.
    """
    try:
        # Identify all placeholders in the template
        placeholders = set(PLACEHOLDER_PATTERN.findall(list_template))
        # Validate that no restricted fields are used
        for field in placeholders:
            if field not in ALLOWED_FIELDS:
                raise ValueError(
                    f"Restricted field '{field}' used in template. "
                    "Only name, position, and department are allowed."
                )

        # Retrieve all employees from the global registry or data source
        # For demonstration, we assume a function `get_all_employees()` exists.
        # Replace this with the actual data retrieval mechanism in your codebase.
        employees = get_all_employees()  # type: ignore

        # Filter employees by department
        filtered = [
            emp for emp in employees if getattr(emp, "department", None) == team_name
        ]

        # Build formatted lines for each employee
        lines: List[str] = []
        for emp in filtered:
            context = {
                field: getattr(emp, field) for field in placeholders
            }
            try:
                line = list_template.format(employee=context)
            except Exception as e:  # pragma: no cover
                raise ValueError(
                    f"Error formatting template for employee '{emp.name}': {e}"
                ) from e
            lines.append(line)

        return "\n".join(lines)

    except ValueError:
        # Re‑raise validation errors directly
        raise
    except Exception as exc:  # pragma: no cover
        # Any other unexpected exception is wrapped in ValueError
        raise ValueError(f"Unexpected error during worker list construction: {exc}") from exc

# ----------------------------------------------------------------------
# Helper function for demonstration purposes
# Replace or remove this in the actual production environment.
def get_all_employees():
    """
    Dummy implementation returning a list of Employee instances.
    In real usage, replace this with the actual data source (e.g., database query).
    """
    from dataclasses import dataclass

    @dataclass
    class Employee:
        name: str
        position: str
        department: str
        salary: float  # Restricted field
        personal_email: str  # Restricted field

    return [
        Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@company.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
        Employee("Carol Williams", "Analyst", "Finance", 80000, "carol@company.com"),
    ]