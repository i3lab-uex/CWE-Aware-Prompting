import re
from typing import List

# ------------------------------------------------------------
# Assume the existence of an Employee data class somewhere in the codebase.
# For demonstration purposes, a minimal mock implementation is provided below.
# ------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = 0.0, personal_email: str = ""):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------
# Mock repository of employees. In a real system this would be
# replaced by database access or another data source.
# ------------------------------------------------------------
def get_all_employees() -> List[Employee]:
    return [
        Employee("Alice Smith", "Engineer", "R&D", 90000, "alice@company.com"),
        Employee("Bob Johnson", "Senior Engineer", "R&D", 110000, "bob@company.com"),
        Employee("Carol Lee", "HR Manager", "Human Resources", 80000, "carol@company.com"),
    ]

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted directory listing for employees belonging to the
    specified department.

    Parameters
    ----------
    dep : str
        The target department.
    format_template : str
        A template string containing placeholders such as {employee.name}
        or {employee.position}.

    Returns
    -------
    str
        A string containing the formatted directory listing, one employee per line.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Define allowed fields
    SAFE_FIELDS = {"name", "position", "department"}

    # Compile regex to find placeholders of the form {employee.<field>}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_]+)\}")

    # Check for disallowed placeholders before processing
    for match in placeholder_pattern.finditer(format_template):
        field = match.group(1)
        if field not in SAFE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is prohibited.")

    # Retrieve employees and filter by department
    all_emps = get_all_employees()
    filtered_emps = [e for e in all_emps if e.department == dep]

    # If no employees found, return an empty string
    if not filtered_emps:
        return ""

    # Function to replace placeholders for a single employee
    def _format_for_employee(emp: Employee) -> str:
        try:
            # Use a simple replacement loop
            result = format_template
            for field in SAFE_FIELDS:
                placeholder = f"{{employee.{field}}}"
                value = getattr(emp, field)
                result = result.replace(placeholder, str(value))
            return result
        except Exception as exc:
            # Any unexpected error during formatting triggers a ValueError
            raise ValueError(f"Formatting failed for employee '{emp.name}': {exc}") from exc

    # Build the final directory listing
    formatted_lines = [_format_for_employee(e) for e in filtered_emps]
    return "\n".join(formatted_lines)

# ------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_staff_listing("R&D", template))