import string
from typing import List

# --------------------------------------------------------------------------- #
# Dummy Employee class (in real usage this would be imported from your models)
# --------------------------------------------------------------------------- #
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# --------------------------------------------------------------------------- #
# Example employee list – replace or populate this from your data source
# --------------------------------------------------------------------------- #
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Jones", "Manager", "Engineering", 120000, "bob.jones@company.com"),
    Employee("Carol White", "Analyst", "Finance", 80000, "carol.white@company.com"),
    # Add more employees as needed
]

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted directory string for all employees in the given division.
    
    Parameters
    ----------
    division : str
        The department name to filter employees by.
    template_str : str
        A format string containing placeholders such as '{employee.name}' or
        '{employee.position}'.  The function substitutes these with the
        corresponding attributes of each employee in the selected division.
    
    Returns
    -------
    str
        A single string containing one formatted entry per employee, separated by newlines.
    
    Raises
    ------
    ValueError
        If the template attempts to access sensitive attributes (salary or personal_email)
        or if any error occurs during formatting.
    """
    # 1. Detect disallowed placeholders
    disallowed = {"salary", "personal_email"}
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template_str):
        if field_name is None:
            continue
        # Split on '.' to allow nested attributes (e.g., employee.name)
        parts = field_name.split(".")
        if len(parts) > 1 and parts[1] in disallowed:
            raise ValueError(f"Access to sensitive attribute '{parts[1]}' is not permitted.")
    
    # 2. Filter employees by division
    filtered = [emp for emp in EMPLOYEES if emp.department == division]
    
    # 3. Format each employee record
    formatted_entries = []
    for emp in filtered:
        try:
            entry = template_str.format(employee=emp)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Error formatting entry for employee '{emp.name}': {exc}") from exc
        formatted_entries.append(entry)
    
    # 4. Join entries with newlines
    return "\n".join(formatted_entries)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(compile_department_roster("Engineering", tmpl))