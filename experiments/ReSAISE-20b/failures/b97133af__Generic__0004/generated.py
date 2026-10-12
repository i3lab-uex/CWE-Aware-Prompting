import re
from typing import List

# -------------------------------------------------------------
# Example Employee class (in real use case this would be imported)
# -------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# -------------------------------------------------------------
# Dummy data for illustration – in real usage this list would be
# provided by the surrounding application or a database query.
# -------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "R&D", 95000.0, "alice@example.com"),
    Employee("Bob Johnson", "Manager", "R&D", 120000.0, "bob@example.com"),
    Employee("Charlie Lee", "Analyst", "Finance", 68000.0, "charlie@example.com"),
]

# -------------------------------------------------------------
# Utility function: safe formatting of a single employee
# -------------------------------------------------------------
_SENSITIVE_FIELDS = {"salary", "personal_email"}

def _format_employee(template: str, employee: Employee) -> str:
    """
    Replace placeholders in the form {employee.<attr>} with actual values.
    Raises ValueError if a sensitive field is requested or an unknown
    attribute is accessed.
    """
    # Find all placeholders of the form {employee.<attr>}
    pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    result = template

    for match in pattern.finditer(template):
        attr_name = match.group(1)

        # Disallow sensitive data
        if attr_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{attr_name}' is prohibited.")

        # Ensure the attribute exists
        if not hasattr(employee, attr_name):
            raise ValueError(f"Employee has no attribute '{attr_name}'.")

        # Retrieve the value and convert to string
        value = getattr(employee, attr_name)
        result = result.replace(match.group(0), str(value))

    return result

# -------------------------------------------------------------
# Main function
# -------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory string for all employees in the
    specified department.

    Parameters:
        dept_name (str): The name of the department to filter by.
        dir_template (str): A template string containing placeholders
                            like '{employee.name}'.

    Returns:
        str: The concatenated formatted directory for the department.

    Raises:
        ValueError: If a sensitive field is requested or any other
                    error occurs during processing.
    """
    if not isinstance(dept_name, str) or not isinstance(dir_template, str):
        raise ValueError("Both 'dept_name' and 'dir_template' must be strings.")

    # Filter employees by department (case-insensitive match)
    dept_employees = [
        emp for emp in EMPLOYEES
        if getattr(emp, "department", "").lower() == dept_name.lower()
    ]

    if not dept_employees:
        return f"No employees found in department '{dept_name}'."

    formatted_entries = []
    for emp in dept_employees:
        try:
            entry = _format_employee(dir_template, emp)
        except Exception as exc:  # Catch all exceptions from formatting
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        formatted_entries.append(entry)

    # Join entries with a newline separator
    return "\n".join(formatted_entries)


# -------------------------------------------------------------
# Example usage (uncomment to test)
# -------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_department_directory("R&D", template))