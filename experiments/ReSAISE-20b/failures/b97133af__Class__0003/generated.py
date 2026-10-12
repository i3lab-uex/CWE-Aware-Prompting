import re
from typing import List

# Minimal Employee class for demonstration; in real use this would be provided elsewhere
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Sample data store (replace with actual data source in production)
_EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 75000, "carol@company.com"),
]

# Forbidden attribute names that must not appear in the template
_FORBIDDEN_PLACEHOLDERS = {"salary", "personal_email"}

def _check_template_security(template: str) -> None:
    """
    Verify that the template does not reference any forbidden placeholders.
    Raises ValueError if a forbidden placeholder is found.
    """
    # Find all {something} placeholders
    placeholders = re.findall(r"{([^{}]+)}", template)
    for ph in placeholders:
        # Handle nested attribute access like employee.salary
        parts = [p.strip() for p in ph.split(".")]
        if any(part in _FORBIDDEN_PLACEHOLDERS for part in parts):
            raise ValueError(f"Template contains forbidden placeholder: {{{ph}}}")

def _format_employee(template: str, employee: Employee) -> str:
    """
    Safely format the template for a single employee.
    Raises ValueError if formatting fails due to missing attributes or other errors.
    """
    try:
        # Use a local namespace where 'employee' refers to the employee instance
        return template.format(employee=employee)
    except (KeyError, AttributeError, IndexError, ValueError) as exc:
        raise ValueError(f"Error formatting template for employee {employee.name}: {exc}") from exc

def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as '{employee.name}'
        or '{employee.position}' to be replaced with actual employee data.

    Returns
    -------
    str
        A single string containing the formatted directory entries for all employees
        in the specified department, separated by newlines. If no employees match,
        an empty string is returned.

    Raises
    ------
    ValueError
        If the template references sensitive attributes (salary or personal_email)
        or if any error occurs during formatting.
    """
    # Security check for forbidden placeholders
    _check_template_security(dir_template)

    # Filter employees by department (case‑insensitive match)
    filtered = [emp for emp in _EMPLOYEES if emp.department.lower() == dept_name.lower()]

    # Format each employee entry
    formatted_entries = [_format_employee(dir_template, emp) for emp in filtered]

    # Join entries with newline separator
    return "\n".join(formatted_entries)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_department_directory("Engineering", template))