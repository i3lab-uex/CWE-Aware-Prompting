import re
from typing import List, Dict

# --------------------------------------------------------------------------- #
# Mock Employee class (replace with the actual implementation in production)
# --------------------------------------------------------------------------- #
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------------- #
# Global employee repository (replace with actual data source)
# --------------------------------------------------------------------------- #
EMPLOYEES: List[Employee] = [
    Employee("Alice Johnson", "Software Engineer", "Engineering", 95000, "alice.johnson@company.com"),
    Employee("Bob Smith", "Product Manager", "Engineering", 105000, "bob.smith@company.com"),
    Employee("Carol White", "HR Specialist", "Human Resources", 70000, "carol.white@company.com"),
    # Add more employees as needed
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _extract_placeholders(template: str) -> List[str]:
    """
    Extracts all placeholder names from a format string.
    Example: "{employee.name} works as {employee.position}" -> ["name", "position"]
    """
    return re.findall(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", template)

def _validate_template(placeholders: List[str]) -> None:
    """
    Raises ValueError if the template contains placeholders for sensitive data.
    Sensitive fields: salary, personal_email
    """
    sensitive = {"salary", "personal_email"}
    for field in placeholders:
        if field.lower() in sensitive:
            raise ValueError(f"Access to sensitive field '{field}' is not allowed.")

def _employee_to_dict(emp: Employee) -> Dict[str, str]:
    """
    Convert an employee object to a dictionary suitable for string formatting.
    Only non-sensitive fields are exposed.
    """
    return {
        "name": emp.name,
        "position": emp.position,
        "department": emp.department,
    }

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def create_employee_directory(department: str, template: str) -> str:
    """
    Generates a directory string for all employees in the given department
    using the provided template.

    Args:
        department (str): The name of the department.
        template (str): A format string containing placeholders like
                        '{employee.name}', '{employee.position}'.

    Returns:
        str: The concatenated directory entries, one per line.

    Raises:
        ValueError: If the template contains disallowed placeholders or
                    any other error occurs during processing.
    """
    if not isinstance(department, str) or not isinstance(template, str):
        raise ValueError("Both 'department' and 'template' must be strings.")

    # 1. Validate template placeholders
    placeholders = _extract_placeholders(template)
    _validate_template(placeholders)

    # 2. Filter employees by department
    matching = [emp for emp in EMPLOYEES if emp.department.lower() == department.lower()]
    if not matching:
        return f"No employees found in department '{department}'."

    # 3. Build directory entries
    lines = []
    for emp in matching:
        try:
            mapping = _employee_to_dict(emp)
            line = template.format(employee=mapping)
        except Exception as exc:
            raise ValueError(f"Failed to format entry for employee '{emp.name}': {exc}") from exc
        lines.append(line)

    # 4. Return the joined directory string
    return "\n".join(lines)