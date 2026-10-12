import re
from typing import List

# --------------------------------------------------------------
# Employee data model (simplified for this example)
# --------------------------------------------------------------

class Employee:
    """
    Represents an employee in the organization.
    Only public attributes are allowed to be exposed through templates.
    """
    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------
# Mock data store
# --------------------------------------------------------------

# In a real system this would come from a database or an API.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "DevOps Engineer", "Engineering", 88000.0, "bob.johnson@example.com"),
    Employee("Carol Williams", "Product Manager", "Engineering", 105000.0, "carol.williams@example.com"),
    Employee("David Brown", "HR Specialist", "Human Resources", 70000.0, "david.brown@example.com"),
    Employee("Eve Davis", "Recruiter", "Human Resources", 65000.0, "eve.davis@example.com"),
]

# --------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------

def _get_department_employees(department: str) -> List[Employee]:
    """
    Retrieve all employees belonging to a specific department.
    Raises ValueError if the department does not exist or no employees are found.
    """
    dept_emps = [e for e in EMPLOYEES if e.department.lower() == department.lower()]
    if not dept_emps:
        raise ValueError(f"No employees found in department '{department}'.")
    return dept_emps

# --------------------------------------------------------------
# Main function
# --------------------------------------------------------------

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department
    using the provided template.

    Parameters:
        department (str): Name of the department.
        template (str): Template string containing placeholders like
                        '{employee.name}' or '{employee.position}'.

    Returns:
        str: The formatted directory string with one line per employee.

    Raises:
        ValueError: If the department has no employees, if the template
                    contains disallowed placeholders (e.g., salary or personal_email),
                    or if any other error occurs during processing.
    """
    # Validate that the template does not expose sensitive data
    disallowed = {"salary", "personal_email"}
    placeholder_pattern = r"{employee\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    placeholders = re.findall(placeholder_pattern, template)

    for ph in placeholders:
        if ph in disallowed:
            raise ValueError(f"Template contains disallowed placeholder '{{employee.{ph}}}'.")

    # Retrieve employees for the department
    try:
        dept_employees = _get_department_employees(department)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to retrieve employees for department '{department}': {exc}") from exc

    # Build directory lines
    directory_lines = []
    for emp in dept_employees:
        try:
            # Replace placeholders with actual data
            line = template.format(employee=emp)
            directory_lines.append(line)
        except AttributeError as exc:  # pragma: no cover
            raise ValueError(f"Invalid placeholder in template: {exc}") from exc
        except KeyError as exc:  # pragma: no cover
            raise ValueError(f"Missing attribute in employee data: {exc}") from exc

    # Join lines with newline separator
    return "\n".join(directory_lines)

# --------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------

if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(create_employee_directory("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")