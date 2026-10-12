import re
from typing import List, Any

# Example Employee class (for context – in real usage this would be imported)
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global employee list (placeholder – replace with actual data source)
EMPLOYEES: List[Employee] = []

def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted directory for employees in the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees.
    dir_template : str
        A template string containing placeholders such as '{employee.name}'
        or '{employee.position}' to be replaced with actual employee data.

    Returns
    -------
    str
        The formatted directory string for the selected department.

    Raises
    ------
    ValueError
        If a placeholder attempts to access sensitive attributes (salary or personal_email)
        or if any other error occurs during processing.
    """
    # Regular expression to find placeholders like {employee.attribute}
    placeholder_pattern = re.compile(r'\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}')

    # Filter employees by department
    try:
        dept_employees = [e for e in EMPLOYEES if e.department == dept_name]
    except Exception as exc:
        raise ValueError(f"Error filtering employees by department: {exc}") from exc

    # Prepare a list to hold each employee's formatted string
    formatted_entries: List[str] = []

    for emp in dept_employees:
        try:
            # Function to replace each placeholder
            def _replace(match: re.Match) -> str:
                attr = match.group(1)
                # Prevent access to sensitive attributes
                if attr in {'salary', 'personal_email'}:
                    raise ValueError(f"Access to sensitive attribute '{attr}' is forbidden.")
                # Get the attribute value; raise if missing
                try:
                    value = getattr(emp, attr)
                except AttributeError as exc:
                    raise ValueError(f"Employee has no attribute '{attr}'.") from exc
                return str(value)

            # Perform substitution on the template for this employee
            entry = placeholder_pattern.sub(_replace, dir_template)
            formatted_entries.append(entry)
        except Exception as exc:
            # Wrap any exception as ValueError with context
            raise ValueError(f"Failed to format entry for employee '{emp.name}': {exc}") from exc

    # Join all entries with a newline (or any other separator you prefer)
    return "\n".join(formatted_entries)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     EMPLOYEES = [
#         Employee("Alice", "Engineer", "Engineering", 95000, "alice@example.com"),
#         Employee("Bob", "Manager", "Engineering", 120000, "bob@example.com"),
#         Employee("Carol", "Analyst", "Finance", 70000, "carol@example.com")
#     ]
#     template = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_department_directory("Engineering", template))