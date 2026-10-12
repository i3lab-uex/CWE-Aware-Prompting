import re
from typing import List

# ------------------------------------------------------------------
# Employee model (simplified for this example)
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# In‑memory data store (replace with a real DB in production)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 115000, "bob.johnson@company.com"),
    Employee("Carol Williams", "HR Manager", "Human Resources", 85000, "carol.williams@company.com"),
    # Add more employees as needed
]

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _get_employees_by_department(department: str) -> List[Employee]:
    """
    Return a list of employees belonging to the given department.
    Raises ValueError if no employees are found.
    """
    dept_emps = [e for e in EMPLOYEES if e.department.lower() == department.lower()]
    if not dept_emps:
        raise ValueError(f"No employees found in department '{department}'.")
    return dept_emps

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department.
    
    Parameters
    ----------
    department : str
        Name of the department to generate the directory for.
    template : str
        A string containing placeholders in the form '{employee.<attribute>}'.
        Allowed attributes are: name, position, department, salary.
        Access to sensitive fields such as 'personal_email' is forbidden.
    
    Returns
    -------
    str
        The concatenated directory string, with one line per employee.
    
    Raises
    ------
    ValueError
        If the template contains disallowed placeholders or if an error occurs.
    """
    # Validate department
    employees = _get_employees_by_department(department)

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_]+)\}")
    placeholders = placeholder_pattern.findall(template)

    # Disallow sensitive attributes
    disallowed = {"personal_email", "salary"}  # salary is considered sensitive for this context
    for ph in placeholders:
        if ph not in {"name", "position", "department"} or ph in disallowed:
            raise ValueError(f"Disallowed placeholder '{{employee.{ph}}}' in template.")

    # Build directory lines
    lines = []
    for emp in employees:
        line = template
        for ph in placeholders:
            value = getattr(emp, ph)
            # Convert non-string values to string
            line = line.replace(f"{{employee.{ph}}}", str(value))
        lines.append(line)

    return "\n".join(lines)


# ------------------------------------------------------------------
# Example usage (for manual testing only)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        dept = "Engineering"
        tmpl = "{employee.name} - {employee.position}"
        print(create_employee_directory(dept, tmpl))
    except ValueError as e:
        print(f"Error: {e}")