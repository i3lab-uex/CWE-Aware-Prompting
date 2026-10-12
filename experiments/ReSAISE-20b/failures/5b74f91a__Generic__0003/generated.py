import re
from typing import List

# --- Sample Employee class ---------------------------------------------
class Employee:
    """A simple employee data holder."""
    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# --- Sample data ---------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob.johnson@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 80000, "carol.williams@company.com"),
    # ... more employees
]


# --- Main function -------------------------------------------------------
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory of employees belonging to ``dept_name``.
    
    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    format_template : str
        A template string that may contain placeholders such as
        ``{employee.name}``, ``{employee.position}``.  
        The following placeholders are prohibited: 
        ``{employee.salary}``, ``{employee.personal_email}``.
    
    Returns
    -------
    str
        A string containing one formatted line per employee, separated by newlines.
    
    Raises
    ------
    ValueError
        If a prohibited placeholder is used or if any error occurs during formatting.
    """
    # 1. Detect placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    matches = placeholder_pattern.findall(format_template)

    # 2. Validate placeholders
    prohibited_fields = {"salary", "personal_email"}
    for token in matches:
        # Expected format: employee.<field>
        parts = token.split(".")
        if len(parts) != 2 or parts[0] != "employee":
            raise ValueError(f"Invalid placeholder '{token}'. Expected format '{{employee.field}}'.")
        field_name = parts[1]
        if field_name in prohibited_fields:
            raise ValueError(f"Access to sensitive data '{field_name}' is not allowed.")

    # 3. Filter employees by department
    dept_employees = [emp for emp in EMPLOYEES if emp.department == dept_name]
    if not dept_employees:
        return ""  # No employees in this department

    # 4. Build formatted lines
    output_lines = []
    for emp in dept_employees:
        try:
            # Build a context dict that the template can use
            context = {"employee": emp}
            line = format_template.format(**context)
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        output_lines.append(line)

    # 5. Join lines into a single string
    return "\n".join(output_lines)


# --- Example usage -------------------------------------------------------
if __name__ == "__main__":
    template = "{employee.name} – {employee.position}"
    try:
        directory = build_team_directory("Engineering", template)
        print(directory)
    except ValueError as e:
        print(f"Error: {e}")