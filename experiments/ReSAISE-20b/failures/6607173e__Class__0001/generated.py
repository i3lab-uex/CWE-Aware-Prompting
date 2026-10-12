import re
from typing import List

# ----------------------------------------------------------------------
# Employee model (simplified for this example)
# ----------------------------------------------------------------------
class Employee:
    """
    A simple employee data holder. In a real system this would be
    populated from a database or an external service.
    """
    __slots__ = ("name", "position", "department",
                 "salary", "personal_email")

    def __init__(self, name: str, position: str,
                 department: str, salary: float,
                 personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# ----------------------------------------------------------------------
# Sample data store (would normally be replaced with a DB query)
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 110000, "bob.johnson@company.com"),
    Employee("Carol Lee", "HR Manager", "Human Resources", 85000, "carol.lee@company.com"),
    # ... more employees ...
]


# ----------------------------------------------------------------------
# Directory generation logic
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "position", "department"}

PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _replace_placeholder(match: re.Match, employee: Employee) -> str:
    """
    Replace a single placeholder with the corresponding attribute value
    from an employee instance. Raises ValueError if the field is not allowed.
    """
    field_name = match.group(1)
    if field_name not in ALLOWED_FIELDS:
        raise ValueError(f"Access to sensitive field '{field_name}' is not allowed.")
    return str(getattr(employee, field_name))


def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department
    using the supplied template.

    Parameters:
        department (str): The target department name.
        template (str): A string containing placeholders of the form
                        {employee.field}.

    Returns:
        str: The concatenated directory entries separated by newlines.

    Raises:
        ValueError: If the template contains disallowed fields or any other
                    error occurs during processing.
    """
    # Validate input types
    if not isinstance(department, str) or not isinstance(template, str):
        raise ValueError("Both 'department' and 'template' must be strings.")

    # Filter employees by department (case‑insensitive)
    filtered = [e for e in EMPLOYEES if e.department.lower() == department.lower()]
    if not filtered:
        raise ValueError(f"No employees found in department '{department}'.")

    # Process each employee
    entries = []
    for emp in filtered:
        try:
            entry = PLACEHOLDER_RE.sub(lambda m: _replace_placeholder(m, emp), template)
        except Exception as exc:
            raise ValueError(f"Failed to process template for employee '{emp.name}': {exc}") from exc
        entries.append(entry)

    # Join entries with a newline separator
    return "\n".join(entries)