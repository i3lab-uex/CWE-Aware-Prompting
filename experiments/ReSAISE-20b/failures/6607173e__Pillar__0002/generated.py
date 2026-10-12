import re
from typing import List

# --------------------------------------------------------------------------- #
# Mock data model and global employee registry (would normally come from a DB)
# --------------------------------------------------------------------------- #

class Employee:
    """
    Simple employee data model.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of employees – in a real system this would be fetched from
# persistent storage (e.g., a database or an external service).
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering",
             95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "DevOps Engineer", "Engineering",
             90000.0, "bob.johnson@company.com"),
    Employee("Carol White", "HR Manager", "Human Resources",
             85000.0, "carol.white@company.com"),
    # ... more employees ...
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any disallowed attributes.
    In this system, personal email addresses are considered sensitive and
    cannot be exposed through the directory.
    """
    # Find all placeholders of the form {employee.<attr>}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    for match in placeholder_pattern.finditer(template):
        attr = match.group(1).strip()
        if attr == "personal_email":
            raise ValueError("Access to personal email is prohibited in the template.")
        # Future: add more checks for sensitive attributes here.

def _employee_to_dict(employee: Employee) -> dict:
    """
    Convert an Employee instance into a dictionary suitable for string
    formatting. Excludes sensitive attributes.
    """
    return {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
        "salary": f"{employee.salary:,.2f}",  # formatted for readability
    }

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department.

    Parameters
    ----------
    department : str
        Name of the department to filter employees.
    template : str
        A string containing placeholders like '{employee.name}' or
        '{employee.position}'. The function will replace these placeholders
        with actual data from each employee in the department.

    Returns
    -------
    str
        The concatenated directory string, one entry per employee.

    Raises
    ------
    ValueError
        If the template references disallowed attributes or any other error
        occurs during processing.
    """
    try:
        # 1. Validate the template for security concerns
        _validate_template(template)

        # 2. Filter employees by department (case-insensitive)
        dept_lower = department.strip().lower()
        relevant_employees = [
            emp for emp in EMPLOYEES if emp.department.lower() == dept_lower
        ]

        # 3. Build the directory string
        lines = []
        for emp in relevant_employees:
            emp_dict = _employee_to_dict(emp)
            # Use safe formatting: if a placeholder is missing, raise an error
            try:
                line = template.format(**emp_dict)
            except KeyError as e:
                raise ValueError(f"Template references unknown attribute: {e}") from None
            lines.append(line)

        # 4. Join all lines with a newline separator
        return "\n".join(lines)

    except Exception as exc:
        # Re-raise known ValueError; otherwise wrap into ValueError
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Failed to create employee directory: {exc}") from exc

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove to run in production)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_employee_directory("Engineering", tmpl))