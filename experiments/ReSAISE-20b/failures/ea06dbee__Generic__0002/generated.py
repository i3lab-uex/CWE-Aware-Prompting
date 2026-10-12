import re
from dataclasses import dataclass, asdict
from typing import List

# ----------------------------------------------------------------------
# Dummy data and Employee definition
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float
    personal_email: str

# Example employee list (in a real system this would come from a database)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob.johnson@company.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 70000.0, "carol.lee@company.com"),
    # ... more employees ...
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _sanitize_template(template: str) -> None:
    """
    Ensure the template does not reference sensitive fields.
    Raises ValueError if a forbidden placeholder is found.
    """
    forbidden = {"salary", "personal_email"}
    # Find all placeholders in the form {employee.field}
    for match in re.finditer(r"{\s*employee\.([a-zA-Z_]\w*)\s*}", template):
        field = match.group(1)
        if field in forbidden:
            raise ValueError(f"Access to sensitive field '{field}' is not allowed.")

def _format_employee(emp: Employee, template: str) -> str:
    """
    Format a single employee record using the given template.
    """
    # Convert dataclass to dict for formatting
    data = asdict(emp)
    try:
        return template.format(employee=data)
    except Exception as exc:  # Catch formatting errors
        raise ValueError(f"Template formatting failed for employee '{emp.name}': {exc}") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dep : str
        Department name to filter employees.
    format_template : str
        Template string containing placeholders like {employee.name}.

    Returns
    -------
    str
        Concatenated formatted string of all employees in the department.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data or any formatting error occurs.
    """
    # Validate and sanitize the template first
    _sanitize_template(format_template)

    # Filter employees by department (case‑insensitive)
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dep.lower()]
    if not dept_employees:
        return f"No employees found in department '{dep}'."

    # Build the directory string
    formatted_entries = []
    for emp in dept_employees:
        entry = _format_employee(emp, format_template)
        formatted_entries.append(entry)

    return "\n".join(formatted_entries)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "{employee.name} - {employee.position}"
#     print(generate_staff_listing("Engineering", tmpl))