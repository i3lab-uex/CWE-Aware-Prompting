import re
from dataclasses import dataclass
from typing import List

# --------------------------------------------------------------------------- #
#  Employee model (simplified for this example)
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float            # Sensitive – should never be exposed via the template
    personal_email: str      # Sensitive – should never be exposed via the template

# --------------------------------------------------------------------------- #
#  Sample data set (in a real application this would come from a DB or API)
# --------------------------------------------------------------------------- #
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 115000.0, "bob.johnson@example.com"),
    Employee("Carol White", "HR Manager", "Human Resources", 78000.0, "carol.white@example.com"),
    # ... more employees
]

# --------------------------------------------------------------------------- #
#  Utility functions
# --------------------------------------------------------------------------- #
_SENSITIVE_FIELDS = {"salary", "personal_email"}

def _extract_placeholders(template: str) -> List[str]:
    """
    Extracts the attribute names used in the template.
    e.g. "Hello {employee.name}" -> ["name"]
    """
    return re.findall(r"\{employee\.([^\}]+)\}", template)

def _validate_placeholders(placeholders: List[str]) -> None:
    """
    Raises ValueError if any placeholder refers to sensitive data.
    """
    for field in placeholders:
        if field.lower() in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is not allowed.")
    # Ensure placeholders are valid attributes of Employee
    for field in placeholders:
        if not hasattr(Employee, field):
            raise ValueError(f"Unknown employee attribute '{field}' in template.")

def _replace_placeholders(employee: Employee, template: str) -> str:
    """
    Replaces placeholders in the template with actual employee data.
    """
    def repl(match):
        attr = match.group(1)
        return str(getattr(employee, attr))
    return re.sub(r"\{employee\.([^\}]+)\}", repl, template)

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Generates a formatted directory for all employees in the specified department.
    
    Parameters
    ----------
    dept_name : str
        Name of the department to filter employees by.
    format_template : str
        Template string containing placeholders such as '{employee.name}' or 
        '{employee.position}'. Sensitive fields like salary or personal_email are
        disallowed and will cause a ValueError.
    
    Returns
    -------
    str
        Multi-line string where each line is the formatted representation of an
        employee in the target department.
    
    Raises
    ------
    ValueError
        If the template references a sensitive field or an unknown attribute,
        or if any other error occurs during formatting.
    """
    # 1. Validate placeholders against sensitive fields
    try:
        placeholders = _extract_placeholders(format_template)
        _validate_placeholders(placeholders)
    except Exception as exc:
        raise ValueError(f"Template validation failed: {exc}") from exc

    # 2. Filter employees by department (case-insensitive match)
    filtered = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not filtered:
        return f"No employees found in department '{dept_name}'."

    # 3. Build the directory
    lines = []
    for emp in filtered:
        try:
            line = _replace_placeholders(emp, format_template)
        except Exception as exc:
            raise ValueError(f"Failed to format employee '{emp.name}': {exc}") from exc
        lines.append(line)

    return "\n".join(lines)