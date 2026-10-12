import re
from dataclasses import dataclass
from typing import List

# ----------------------------------------------------------------------
# Employee model (minimal implementation for demonstration)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float  # sensitive
    personal_email: str  # sensitive

# ----------------------------------------------------------------------
# Sample data store (in a real system this would be fetched from a DB)
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 115000, "bob.johnson@example.com"),
    Employee("Carol White", "HR Manager", "Human Resources", 85000, "carol.white@example.com"),
    # ... more employees
]

# ----------------------------------------------------------------------
# Helper: Validate that the template does not request sensitive data
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"salary", "personal_email"}

def _validate_template(template: str) -> None:
    """
    Ensure the template does not contain placeholders for sensitive fields.
    Raises ValueError if a disallowed field is found.
    """
    # Find all placeholders like {employee.field}
    placeholders = re.findall(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", template)
    for field in placeholders:
        if field.lower() in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is not allowed in the template.")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a directory listing for employees in the specified department.
    
    Parameters
    ----------
    dep : str
        The target department name (case-sensitive).
    format_template : str
        A template string containing placeholders such as '{employee.name}'.
    
    Returns
    -------
    str
        A newline-separated string with each employee formatted according to the template.
    
    Raises
    ------
    ValueError
        If the template references a sensitive field or if any formatting error occurs.
    """
    # 1. Validate the template for disallowed fields
    _validate_template(format_template)

    # 2. Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department == dep]
    
    # 3. Format each employee entry
    lines = []
    for emp in dept_employees:
        try:
            # Build a simple namespace dict for formatting
            context = {"employee": emp}
            line = format_template.format(**context)
        except Exception as exc:
            # Any formatting error is treated as a security/logic issue
            raise ValueError(f"Failed to format employee data: {exc}") from exc
        lines.append(line)
    
    # 4. Join with newlines; if no employees, return an empty string
    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_staff_listing("Engineering", template))