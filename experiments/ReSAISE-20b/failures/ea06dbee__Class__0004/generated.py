import re
from typing import List

# --------------------------------------------------------------------------- #
# 1. Domain model (minimal, for demonstration purposes)
# --------------------------------------------------------------------------- #

class Employee:
    """
    Simple representation of an employee.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------------- #
# 2. Sample data source (replace with real persistence layer in production)
# --------------------------------------------------------------------------- #

def _load_employees() -> List[Employee]:
    """
    Load all employees. In a real application this would query a database
    or an external service.
    """
    return [
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
        Employee("Bob Johnson", "Senior Engineer", "Engineering", 120000, "bob@company.com"),
        Employee("Carol White", "HR Manager", "Human Resources", 80000, "carol@company.com"),
        Employee("David Brown", "Accountant", "Finance", 70000, "david@company.com"),
    ]

# --------------------------------------------------------------------------- #
# 3. Core function
# --------------------------------------------------------------------------- #

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted directory listing for all employees in the specified
    department. The `format_template` may contain placeholders such as
    '{employee.name}', '{employee.position}' etc.  The function will raise a
    ValueError if the template attempts to access sensitive data (salary or
    personal_email) or if any other error occurs during formatting.

    Parameters:
        dep (str): Department name to filter employees.
        format_template (str): Template string containing placeholders.

    Returns:
        str: The concatenated formatted directory for the department.

    Raises:
        ValueError: If sensitive fields are accessed or an error occurs.
    """
    # ----------------------------------------------------------------------- #
    # 3.1 Detect sensitive placeholders
    # ----------------------------------------------------------------------- #
    sensitive_fields = {"salary", "personal_email"}
    placeholder_pattern = r"\{employee\.([^\}]+)\}"
    placeholders = set(re.findall(placeholder_pattern, format_template))

    if any(field in sensitive_fields for field in placeholders):
        raise ValueError("Template contains access to sensitive employee data.")

    # ----------------------------------------------------------------------- #
    # 3.2 Load employees and filter by department
    # ----------------------------------------------------------------------- #
    try:
        all_emps = _load_employees()
    except Exception as exc:
        raise ValueError(f"Failed to load employees: {exc}") from exc

    dept_emps = [emp for emp in all_emps if emp.department.lower() == dep.lower()]
    if not dept_emps:
        return f"No employees found in department '{dep}'."

    # ----------------------------------------------------------------------- #
    # 3.3 Render each employee line
    # ----------------------------------------------------------------------- #
    rendered_lines = []
    for emp in dept_emps:
        try:
            # Build a simple namespace for formatting
            ctx = {"employee": emp}
            line = format_template.format(**ctx)
        except Exception as exc:
            raise ValueError(f"Error formatting employee {emp.name}: {exc}") from exc
        rendered_lines.append(line)

    # ----------------------------------------------------------------------- #
    # 3.4 Return final string
    # ----------------------------------------------------------------------- #
    return "\n".join(rendered_lines)

# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    print(generate_staff_listing("Engineering", tmpl))