import re
from dataclasses import dataclass, fields
from typing import List

# --------------------------------------------------------------------
# Domain model
# --------------------------------------------------------------------

@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str  # Sensitive field – should never be exposed

# Example in‑memory employee repository
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 110000.0, "bob.johnson@example.com"),
    Employee("Carol White", "HR Specialist", "Human Resources", 65000.0, "carol.white@example.com"),
]

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def _allowed_attributes() -> set:
    """
    Return a set of attribute names that are permitted to appear in the template.
    """
    # Exclude sensitive fields such as personal_email
    return {f.name for f in fields(Employee) if f.name != "personal_email"}

def _replace_placeholders(template: str, employee: Employee) -> str:
    """
    Replace placeholders in the form {employee.<attr>} with actual employee data.
    Raises ValueError if a disallowed attribute is requested or the placeholder
    syntax is malformed.
    """
    allowed = _allowed_attributes()

    # Regex to find all placeholders of the form {employee.attribute}
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def repl(match: re.Match) -> str:
        attr = match.group(1)
        if attr not in allowed:
            raise ValueError(f"Access to disallowed attribute '{attr}' is prohibited.")
        return str(getattr(employee, attr))

    # Perform replacement
    result = pattern.sub(repl, template)
    return result

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department.
    
    Parameters
    ----------
    department : str
        The name of the department to filter employees.
    template : str
        A string containing placeholders such as '{employee.name}' or
        '{employee.position}'. These will be replaced with the corresponding
        employee attributes.
    
    Returns
    -------
    str
        The concatenated directory entries, one per line. If no employees are
        found for the department an empty string is returned.
    
    Raises
    ------
    ValueError
        If the template contains disallowed attributes, malformed placeholders,
        or any other error occurs during processing.
    """
    if not isinstance(department, str) or not department:
        raise ValueError("Department must be a non‑empty string.")
    if not isinstance(template, str):
        raise ValueError("Template must be a string.")

    # Filter employees by department (case‑insensitive match)
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == department.lower()]

    # If no employees, return an empty string
    if not dept_employees:
        return ""

    # Build directory lines safely
    try:
        entries = [_replace_placeholders(template, emp) for emp in dept_employees]
    except Exception as exc:
        # Wrap any exception into ValueError for consistency
        raise ValueError(f"Failed to generate directory: {exc}") from exc

    # Join entries with newline characters
    return "\n".join(entries)

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(create_employee_directory("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")