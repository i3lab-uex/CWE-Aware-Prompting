import re
from typing import List

# ------------------------------------------------------------------
# Employee data model (simplified)
# ------------------------------------------------------------------
class Employee:
    """
    Represents an employee in the company.
    Attributes
    ----------
    name : str
        Full name of the employee.
    position : str
        Job title.
    department : str
        Department name.
    salary : float
        Annual salary in USD.
    personal_email : str
        Personal email address (sensitive).
    """
    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# ------------------------------------------------------------------
# Global employee registry (would normally come from a database)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Johnson", "Software Engineer", "Engineering",
             95000.0, "alice.johnson@example.com"),
    Employee("Bob Smith", "DevOps Engineer", "Engineering",
             88000.0, "bob.smith@example.com"),
    Employee("Carol Lee", "HR Manager", "Human Resources",
             78000.0, "carol.lee@example.com"),
    # ... more employees ...
]


# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _get_employee_attribute(emp: Employee, attr_name: str):
    """
    Safely retrieve an attribute from an employee instance.
    Raises ValueError if the attribute is not allowed or does not exist.
    """
    # Disallow sensitive attributes
    if attr_name == "personal_email":
        raise ValueError("Access to personal_email is forbidden.")
    if not hasattr(emp, attr_name):
        raise ValueError(f"Attribute '{attr_name}' does not exist on Employee.")
    return getattr(emp, attr_name)


def _render_template(template: str, emp: Employee) -> str:
    """
    Replace placeholders in the template with employee data.
    Placeholders are of the form {employee.attribute}.
    """
    # Find all placeholders
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    matches = pattern.findall(template)

    # Replace each placeholder with the corresponding attribute value
    result = template
    for attr in set(matches):
        try:
            value = _get_employee_attribute(emp, attr)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{{employee.{attr}}}': {exc}") from exc
        # Convert value to string for substitution
        result = result.replace(f"{{employee.{attr}}}", str(value))

    return result


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department.
    
    Parameters
    ----------
    department : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'. These will be replaced with actual data.
    
    Returns
    -------
    str
        A concatenated string containing each employee's information as
        formatted by the template. Each entry is separated by a newline.
    
    Raises
    ------
    ValueError
        If the template contains forbidden or invalid placeholders,
        or if any other error occurs during processing.
    """
    # Validate input types
    if not isinstance(department, str):
        raise ValueError("department must be a string")
    if not isinstance(template, str):
        raise ValueError("template must be a string")

    # Filter employees by department (case‑insensitive)
    dept_emps = [emp for emp in EMPLOYEES
                 if emp.department.lower() == department.lower()]

    if not dept_emps:
        return f"No employees found in department '{department}'."

    # Render each employee's entry
    rendered_entries = []
    for emp in dept_emps:
        try:
            rendered_entries.append(_render_template(template, emp))
        except ValueError as exc:
            # Stop processing on first error to avoid leaking sensitive data
            raise ValueError(f"Failed to render template for employee '{emp.name}': {exc}") from exc

    # Join entries with newlines
    return "\n".join(rendered_entries)


# ------------------------------------------------------------------
# Example usage (commented out – remove to run)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Example template
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        directory = create_employee_directory("Engineering", tmpl)
        print(directory)
    except ValueError as e:
        print(f"Error: {e}")