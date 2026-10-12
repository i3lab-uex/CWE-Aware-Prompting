import re
from typing import List

# --------------------------------------------------------------------
#  Sample data model and global employee list.
# In a real system these would come from a database or other persistence layer.

class Employee:
    """Represents an employee record."""
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of employees for demonstration purposes.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000.0, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000.0, "bob.johnson@example.com"),
    Employee("Carol Williams", "HR Specialist", "Human Resources", 75000.0, "carol.williams@example.com"),
]

# --------------------------------------------------------------------
#  Function to generate an employee directory for a given department.

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the specified department.

    Parameters
    ----------
    department : str
        The name of the department for which to generate a directory.
    template : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'. Placeholders must be limited to the set of
        non‑sensitive attributes defined in ``ALLOWED_FIELDS``.

    Returns
    -------
    str
        A concatenated string containing the directory information for all
        employees in the department.

    Raises
    ------
    ValueError
        If any error occurs, or if the template attempts to access a
        disallowed attribute (e.g. ``personal_email``).
    """
    # 1. Validate that the template does not reference any disallowed fields.
    _validate_template(template)

    # 2. Filter employees belonging to the requested department.
    dept_employees = [e for e in EMPLOYEES if e.department == department]
    if not dept_employees:
        raise ValueError(f"No employees found in department '{department}'.")

    # 3. Render the template for each employee and concatenate.
    directory_entries = []
    for emp in dept_employees:
        entry = _render_template(template, emp)
        directory_entries.append(entry)

    return "\n".join(directory_entries)


# --------------------------------------------------------------------
#  Internal helpers

ALLOWED_FIELDS = {"name", "position", "department", "salary"}

PLACEHOLDER_REGEX = re.compile(r"\{([^{}]+)\}")

def _validate_template(template: str) -> None:
    """
    Ensure that the template only references allowed fields and does not
    contain any unsafe expressions.

    Raises ValueError if a disallowed field is found.
    """
    for match in PLACEHOLDER_REGEX.finditer(template):
        placeholder = match.group(1).strip()
        # Expect format 'employee.<field>'
        if not placeholder.startswith("employee."):
            raise ValueError(f"Invalid placeholder '{placeholder}'. "
                             f"Only 'employee.<field>' syntax is allowed.")
        field = placeholder.split(".", 1)[1]
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Access to disallowed attribute '{field}' is prohibited.")


def _render_template(template: str, employee: Employee) -> str:
    """
    Render the template for a single employee.  Since we have already validated
    that only allowed fields are referenced, this function safely uses a
    mapping dictionary.
    """
    # Build a safe mapping from field name to value
    mapping = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "employee.salary": f"{employee.salary:,.2f}",
    }

    def replacer(match):
        key = match.group(1).strip()
        return str(mapping[key])

    return PLACEHOLDER_REGEX.sub(replacer, template)


# --------------------------------------------------------------------
#  Example usage (commented out – remove comments to run)

# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}, Salary: ${employee.salary}"
#     try:
#         print(create_employee_directory("Engineering", tmpl))
#     except ValueError as e:
#         print(f"Error: {e}")