import re
from typing import List

# --------------------------------------------------------------------------- #
#  Mock Employee class (replace with the real implementation in production)
# --------------------------------------------------------------------------- #
class Employee:
    """
    A minimal representation of an employee.  In real usage this class would
    likely be imported from a dedicated module.
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary          # restricted field
        self.personal_email = personal_email  # restricted field

    @staticmethod
    def get_all() -> List["Employee"]:
        """
        Return a list of all employees.  In production this might query a
        database or read from an external data source.
        """
        # Example data – replace with real data source
        return [
            Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
            Employee("Bob Jones", "Manager", "Engineering", 115000, "bob@company.com"),
            Employee("Carol Lee", "Analyst", "Finance", 75000, "carol@company.com"),
        ]

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders such as '{employee.name}' and
        '{employee.position}'.  The placeholders are replaced with the
        corresponding attributes of each employee.

    Returns
    -------
    str
        A newline‑separated string with each line representing an employee.

    Raises
    ------
    ValueError
        If the template references restricted fields (salary or personal_email)
        or if any other error occurs during formatting.
    """
    # Define restricted attributes that must not be exposed
    RESTRICTED_FIELDS = {"salary", "personal_email"}

    # Compile a regular expression to find all placeholders of the form
    # {employee.<field>}
    placeholder_re = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Validate the template does not reference restricted fields
    for match in placeholder_re.finditer(template):
        field_name = match.group(1)
        if field_name in RESTRICTED_FIELDS:
            raise ValueError(
                f"Template references restricted field '{field_name}'. "
                "Access to this attribute is not allowed."
            )

    # Retrieve employees belonging to the requested department
    all_employees = Employee.get_all()
    filtered_employees = [
        emp for emp in all_employees if emp.department.lower() == dept_name.lower()
    ]

    # If no employees match the department, return an empty string
    if not filtered_employees:
        return ""

    # Build the output by formatting each employee's data into the template
    formatted_lines = []
    for emp in filtered_employees:
        try:
            # The template is evaluated with a simple namespace containing
            # the employee instance.  Any missing attribute will raise an
            # AttributeError which we convert to ValueError for consistency.
            line = template.format(employee=emp)
        except AttributeError as exc:
            raise ValueError(
                f"Missing attribute while formatting employee '{emp.name}': {exc}"
            ) from exc
        except Exception as exc:  # pragma: no cover - defensive programming
            raise ValueError(
                f"Unexpected error while formatting employee '{emp.name}': {exc}"
            ) from exc
        formatted_lines.append(line)

    return "\n".join(formatted_lines)


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        print(assemble_employee_list("Engineering", tmpl))
    except ValueError as e:
        print(f"Error: {e}")