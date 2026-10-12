import re
from typing import List

# ------------------------------------------------------------------
# Employee data model (simplified for this module)
# ------------------------------------------------------------------
class Employee:
    """
    Represents an employee with a subset of attributes that may be exposed
    through the directory.  Only name, position and department are allowed
    for display; salary and personal_email are considered sensitive.
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
# Global registry of employees (would normally come from a database)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 90000, "alice@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@example.com"),
    Employee("Carol White", "Analyst", "Finance", 75000, "carol@example.com"),
    # ... more employees
]


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders in the form '{employee.attribute}'.

    Returns
    -------
    str
        The formatted directory string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary, personal_email)
        or if an unexpected error occurs during rendering.
    """
    # Allowed attributes that can be interpolated
    ALLOWED_ATTRS = {"name", "position", "department"}

    # Pre‑compile a regex that captures placeholders like {employee.name}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

    # Find all placeholders in the template
    placeholders = placeholder_pattern.findall(template)

    # Validate that no restricted fields are requested
    for attr in placeholders:
        if attr not in ALLOWED_ATTRS:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")

    # Filter employees by department (case‑insensitive match)
    filtered = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]

    # If no employees found, return an informative message
    if not filtered:
        return f"No employees found in department '{dept_name}'."

    # Build the output string
    lines = []
    for employee in filtered:
        line = template
        try:
            # Replace each placeholder with the actual attribute value
            for attr in placeholders:
                value = getattr(employee, attr)
                # Escape braces in the replacement value to avoid re‑matching
                escaped_value = str(value).replace("{", "{{").replace("}", "}}")
                line = re.sub(rf"{{\s*employee\.{attr}\s*}}", escaped_value, line)
        except Exception as exc:
            # Any error during rendering is considered a security violation
            raise ValueError(f"Error rendering template for employee '{employee.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)


# ------------------------------------------------------------------
# Example usage (for local testing only)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(assemble_employee_list("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")