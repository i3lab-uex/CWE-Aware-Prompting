import re
from typing import List

# --------------------------------------------------------------------
# Assume this Employee class is provided by the system.
# It contains many attributes, but only a few are safe to expose in
# the directory.  The `personal_email` attribute is considered sensitive.
# --------------------------------------------------------------------
class Employee:
    def __init__(
        self,
        name: str,
        position: str,
        department: str,
        salary: float,
        personal_email: str
    ):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

    # In a real system there would be many more attributes and methods.
# --------------------------------------------------------------------


def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department.

    Parameters
    ----------
    department : str
        The name of the department whose employees should be listed.
    template : str
        A string containing placeholders in the form '{employee.<attr>}'.
        Allowed attributes are: name, position, department, salary.

    Returns
    -------
    str
        The directory string with one formatted line per employee,
        separated by newlines.

    Raises
    ------
    ValueError
        If the template contains an unsupported placeholder, if a
        sensitive attribute (e.g. personal_email) is accessed,
        or if any other error occurs during formatting.
    """
    # --------------------------------------------------------------------
    # Step 1: Gather employees belonging to the requested department.
    # In a real application this would query a database or an API.
    # Here we use a placeholder list for demonstration purposes.
    # --------------------------------------------------------------------
    all_employees: List[Employee] = _get_all_employees()
    dept_employees = [
        emp for emp in all_employees if emp.department.lower() == department.lower()
    ]

    if not dept_employees:
        raise ValueError(f"No employees found in department '{department}'")

    # --------------------------------------------------------------------
    # Step 2: Validate the template for disallowed placeholders.
    # Allowed attributes are explicitly listed below.
    # --------------------------------------------------------------------
    allowed_attrs = {"name", "position", "department", "salary"}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    for match in placeholder_pattern.finditer(template):
        attr = match.group(1)
        if attr not in allowed_attrs:
            raise ValueError(
                f"Disallowed placeholder '{{employee.{attr}}}' in template"
            )

    # --------------------------------------------------------------------
    # Step 3: Build the directory string.
    # We replace placeholders manually to avoid using eval or
    # str.format with a potentially unsafe namespace.
    # --------------------------------------------------------------------
    lines = []
    for emp in dept_employees:
        line = template
        for match in placeholder_pattern.finditer(template):
            attr = match.group(1)
            value = getattr(emp, attr)
            # Convert non-string values to string
            if not isinstance(value, str):
                value = str(value)
            # Replace the placeholder with the actual value
            line = line.replace(match.group(0), value)
        lines.append(line)

    return "\n".join(lines)


# --------------------------------------------------------------------
# Helper function to simulate data retrieval.
# In production, replace this with actual data access logic.
# --------------------------------------------------------------------
def _get_all_employees() -> List[Employee]:
    # Example data; in a real system this would come from a database.
    return [
        Employee(
            name="Alice Johnson",
            position="Software Engineer",
            department="Engineering",
            salary=95000.0,
            personal_email="alice.johnson@example.com",
        ),
        Employee(
            name="Bob Smith",
            position="DevOps Engineer",
            department="Engineering",
            salary=88000.0,
            personal_email="bob.smith@example.com",
        ),
        Employee(
            name="Carol Lee",
            position="HR Manager",
            department="Human Resources",
            salary=105000.0,
            personal_email="carol.lee@example.com",
        ),
    ]


# --------------------------------------------------------------------
# Example usage (commented out to avoid side effects when imported).
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(create_employee_directory("Engineering", tmpl))