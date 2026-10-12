import re
from dataclasses import dataclass, field
from typing import List

# ------------------------------------------------------------------
# Employee model (normally this would be provided elsewhere)
# ------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float = field(repr=False)
    personal_email: str = field(repr=False)

# ------------------------------------------------------------------
# Sample data store (replace with real data source in production)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 115000.0, "bob.johnson@company.com"),
    Employee("Carol Williams", "HR Manager", "Human Resources", 80000.0, "carol.williams@company.com"),
    # Add more employees as needed...
]

# ------------------------------------------------------------------
# Directory builder
# ------------------------------------------------------------------
def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory of employees belonging to ``dept_name``.
    
    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    format_template : str
        Template string containing placeholders such as `{employee.name}` or
        `{employee.position}`. Sensitive fields (`salary`, `personal_email`) are
        disallowed.
    
    Returns
    -------
    str
        The concatenated directory string, one employee per line.
    
    Raises
    ------
    ValueError
        If the template references a sensitive field or if formatting fails.
    """
    
    # ------------------------------------------------------------------
    # 1. Validate template for disallowed placeholders
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r'\{employee\.([^\}]+)\}')
    placeholders = placeholder_pattern.findall(format_template)
    
    for field_name in placeholders:
        if field_name in {"salary", "personal_email"}:
            raise ValueError(f"Access to sensitive data '{field_name}' is prohibited.")
    
    # ------------------------------------------------------------------
    # 2. Filter employees by department
    # ------------------------------------------------------------------
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    
    # ------------------------------------------------------------------
    # 3. Format each employee entry
    # ------------------------------------------------------------------
    formatted_entries = []
    for emp in dept_employees:
        try:
            entry = format_template.format(employee=emp)
        except Exception as exc:  # Catch any formatting errors
            raise ValueError(f"Formatting error for employee '{emp.name}': {exc}") from exc
        formatted_entries.append(entry)
    
    # ------------------------------------------------------------------
    # 4. Return the joined directory
    # ------------------------------------------------------------------
    return "\n".join(formatted_entries)

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(build_team_directory("Engineering", template))