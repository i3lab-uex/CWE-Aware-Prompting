import re
from typing import List

# Assume an Employee class is defined elsewhere with the following attributes.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example data store – in real usage this would come from a database or other source.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 115000, "bob.johnson@example.com"),
    Employee("Carol Lee", "Analyst", "Finance", 72000, "carol.lee@example.com"),
    # ... more employees ...
]

# ---------------------------------------------------------------------------

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a directory listing for employees in the specified department.
    
    Parameters
    ----------
    dep : str
        The department whose employees should be included in the listing.
    format_template : str
        A string containing placeholders such as '{employee.name}' or 
        '{employee.position}'.  The placeholders are replaced with the
        corresponding attribute values of each employee.
    
    Returns
    -------
    str
        A newline‑separated string containing the formatted information for
        each employee in the department.
    
    Raises
    ------
    ValueError
        If the template attempts to access a restricted attribute 
        (salary or personal_email) or if any error occurs during formatting.
    """
    
    # Disallowed placeholders that expose sensitive data
    restricted_fields = {"salary", "personal_email"}
    
    # Find all placeholders of the form {employee.<field>}
    placeholder_pattern = r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    found_fields = set(re.findall(placeholder_pattern, format_template))
    
    # Check for restricted fields
    if restricted_fields & found_fields:
        raise ValueError("Template attempts to access sensitive employee data.")
    
    # Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dep.lower()]
    
    # If no employees found, return an empty string
    if not dept_employees:
        return ""
    
    # Build the formatted listing
    lines = []
    for emp in dept_employees:
        try:
            # Prepare a simple namespace with the employee instance
            formatted_line = format_template.format(employee=emp)
        except Exception as exc:
            # Any formatting error is considered a security risk
            raise ValueError(f"Error while formatting employee data: {exc}") from exc
        lines.append(formatted_line)
    
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Example usage (uncomment to test):
#
# template = "{employee.name} - {employee.position}"
# print(generate_staff_listing("Engineering", template))