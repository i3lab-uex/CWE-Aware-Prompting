import re
from dataclasses import dataclass
from typing import List

# ----------------------------------------------------------------------
# Employee data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Sensitive – must not be exposed
    personal_email: str   # Sensitive – must not be exposed

# ----------------------------------------------------------------------
# Sample employee registry (in a real system this would come from a DB)
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Senior Engineer", "Engineering", 120000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Junior Engineer", "Engineering", 85000, "bob.johnson@company.com"),
    Employee("Carol Lee", "HR Manager", "Human Resources", 95000, "carol.lee@company.com"),
    Employee("David Kim", "Recruiter", "Human Resources", 70000, "david.kim@company.com"),
]

# ----------------------------------------------------------------------
# Allowed placeholders
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "position", "department"}

PLACEHOLDER_RE = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department.
    
    Parameters
    ----------
    department : str
        The target department name.
    template : str
        A string containing placeholders such as '{employee.name}'.
    
    Returns
    -------
    str
        The directory string with placeholders replaced by actual data.
    
    Raises
    ------
    ValueError
        If the department is empty, no employees are found,
        a placeholder references sensitive data or an unknown attribute.
    """
    
    if not department:
        raise ValueError("Department name must be provided.")
    
    # Filter employees belonging to the requested department
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == department.lower()]
    if not dept_employees:
        raise ValueError(f"No employees found in department '{department}'.")
    
    # Validate template placeholders
    for match in PLACEHOLDER_RE.finditer(template):
        field = match.group(1)
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unknown field '{field}' is not allowed.")
    
    # Build directory string
    lines = []
    for emp in dept_employees:
        # Prepare a mapping of allowed attributes
        data = {field: getattr(emp, field) for field in ALLOWED_FIELDS}
        try:
            line = template.format(**data)
        except KeyError as exc:
            # Should not happen due to earlier validation
            raise ValueError(f"Missing placeholder data: {exc}") from exc
        lines.append(line)
    
    return "\n".join(lines)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_employee_directory("Engineering", tmpl))