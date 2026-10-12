import re
from typing import List

# ------------------------------------------------------------------
# Mocked Employee class and data repository (replace with real ones)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example in‑memory employee store (replace with DB queries, etc.)
EMPLOYEE_STORE: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 115000, "bob.johnson@company.com"),
    Employee("Carol Williams", "HR Manager", "Human Resources", 85000, "carol.williams@company.com"),
]

def get_employees_by_department(department: str) -> List[Employee]:
    """Return all employees belonging to the given department."""
    return [e for e in EMPLOYEE_STORE if e.department == department]


# ------------------------------------------------------------------
# Directory generation logic
# ------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "position", "department", "salary"}

PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _replace_placeholders(template: str, employee: Employee) -> str:
    """
    Replace placeholders in the template with values from the given
    employee instance. Raises ValueError if a forbidden field is used.
    """
    def repl(match: re.Match) -> str:
        attr = match.group(1)
        if attr not in ALLOWED_FIELDS:
            raise ValueError(f"Access to forbidden field '{attr}' is not allowed.")
        value = getattr(employee, attr)
        return str(value)

    return PLACEHOLDER_RE.sub(repl, template)


def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified
    department using the provided template.

    Parameters:
        department (str): Name of the department.
        template (str): Directory template containing placeholders
                        like '{employee.name}', '{employee.position}',
                        etc.

    Returns:
        str: The generated directory string, with one entry per line.

    Raises:
        ValueError: If the template contains disallowed fields or
                    any other error occurs during processing.
    """
    if not isinstance(department, str) or not isinstance(template, str):
        raise ValueError("Both 'department' and 'template' must be strings.")

    employees = get_employees_by_department(department)
    if not employees:
        return f"No employees found in department '{department}'."

    lines = []
    for emp in employees:
        try:
            line = _replace_placeholders(template, emp)
        except Exception as exc:
            raise ValueError(f"Failed to process template for employee '{emp.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}, Salary: ${employee.salary}"
    print(create_employee_directory("Engineering", tmpl))