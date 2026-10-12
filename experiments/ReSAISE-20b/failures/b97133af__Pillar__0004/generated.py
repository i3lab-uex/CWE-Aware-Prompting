import re
from typing import List

# ------------------------------------------------------------------
# Example Employee class – in real usage this would be imported from
# the application codebase.  The implementation only uses attributes
# that are safe to expose (name, position, department, salary,
# personal_email).
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
# Sample data – in a real system this would come from a database
# or another persistent store.  It is kept here only for demonstration.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000, "bob.johnson@company.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 70000, "carol.lee@company.com"),
]

# ------------------------------------------------------------------
# Helper function to safely format a string with employee attributes
# ------------------------------------------------------------------
def _safe_format(template: str, employee: Employee) -> str:
    """
    Replace placeholders in *template* with values from *employee*.
    Raises ValueError if the template contains any disallowed keys
    (salary or personal_email) or if an attribute is missing.
    """
    # Detect all placeholders in the form {something}
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    placeholders = set(placeholder_pattern.findall(template))

    # Reject any sensitive attributes
    disallowed_keys = {"salary", "personal_email"}
    if placeholders & disallowed_keys:
        raise ValueError(f"Template contains disallowed keys: {placeholders & disallowed_keys}")

    # Build a mapping of allowed attributes
    safe_attrs = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
    }

    # Ensure all placeholders are valid keys
    if not placeholders.issubset(safe_attrs.keys()):
        missing = placeholders - safe_attrs.keys()
        raise ValueError(f"Template contains unknown keys: {missing}")

    try:
        return template.format(**safe_attrs)
    except Exception as exc:
        # Wrap any formatting errors in ValueError for consistency
        raise ValueError(f"Formatting error: {exc}") from exc

# ------------------------------------------------------------------
# Main public function
# ------------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as
        '{employee.name}' or '{employee.position}'.  The function
        replaces these placeholders with the corresponding employee
        attributes.

    Returns
    -------
    str
        The concatenated directory entries for all employees in the
        specified department.

    Raises
    ------
    ValueError
        If the template references disallowed attributes (salary or
        personal_email), if a placeholder refers to an unknown key,
        or if any other error occurs during formatting.
    """
    # Normalise department name for comparison
    dept_name = dept_name.strip().lower()

    # Filter employees by department (case-insensitive)
    selected_employees = [
        e for e in EMPLOYEES if e.department.strip().lower() == dept_name
    ]

    if not selected_employees:
        raise ValueError(f"No employees found in department '{dept_name}'")

    # Replace placeholder prefixes (e.g., 'employee.name') with just the key
    # for easier formatting.  The template may use either style.
    cleaned_template = re.sub(r"{employee\.([^{}]+)}", r"{\1}", dir_template)

    # Format each employee and collect the results
    formatted_entries = []
    for emp in selected_employees:
        entry = _safe_format(cleaned_template, emp)
        formatted_entries.append(entry)

    # Join entries with newlines (or any separator you prefer)
    return "\n".join(formatted_entries)

# ------------------------------------------------------------------
# Example usage (uncomment to test):
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Name: {employee.name}\nPosition: {employee.position}\n"
#     print(generate_department_directory("Engineering", template))