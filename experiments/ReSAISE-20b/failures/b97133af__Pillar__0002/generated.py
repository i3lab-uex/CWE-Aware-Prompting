import re
from typing import List

# ----------------------------------------------------------------------
# Assume an Employee class is defined elsewhere with the following
# attributes: name, position, department, salary, personal_email.
# For completeness we provide a minimal stub that can be replaced by
# the real implementation in the production environment.
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ----------------------------------------------------------------------
# A global list of employees. In a real application this would be
# fetched from a database or another data source.
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ----------------------------------------------------------------------
# Utility function to safely format a template with employee data.
# ----------------------------------------------------------------------
def _safe_format(template: str, mapping: dict) -> str:
    """
    Format *template* using only the keys present in *mapping*.
    Raise ValueError if any key is missing or if a KeyError occurs
    during formatting.
    """
    try:
        return template.format(**mapping)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for {exc}") from None
    except Exception as exc:
        # Catch any other formatting errors (e.g. syntax issues)
        raise ValueError(f"Template formatting error: {exc}") from None


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_department_directory(dept_name: str, dir_template: str) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    dir_template : str
        A template string containing placeholders such as '{employee.name}'
        or '{employee.position}'.  Only the attributes 'name', 'position',
        and 'department' are allowed. Attempting to access 'salary' or
        'personal_email' will raise a ValueError.

    Returns
    -------
    str
        A newline‑separated string where each line contains the formatted
        information for an employee in the selected department.

    Raises
    ------
    ValueError
        If the template contains a disallowed placeholder, if any employee
        lacks a required attribute, or if an unexpected error occurs.
    """
    # ------------------------------------------------------------------
    # 1. Validate template placeholders
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r'{([^}]+)}')
    disallowed_attrs = {'salary', 'personal_email'}

    for match in placeholder_pattern.finditer(dir_template):
        attr = match.group(1)
        # Allow only simple attribute names (no nested access or formatting)
        if '.' in attr:
            raise ValueError(f"Invalid placeholder '{attr}'. Nested attributes are not allowed.")
        if attr in disallowed_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited.")
        if attr not in {'name', 'position', 'department'}:
            raise ValueError(f"Unknown placeholder '{attr}'. Only name, position, and department are allowed.")

    # ------------------------------------------------------------------
    # 2. Filter employees by department
    # ------------------------------------------------------------------
    selected = [e for e in EMPLOYEES if e.department == dept_name]

    # ------------------------------------------------------------------
    # 3. Build formatted lines
    # ------------------------------------------------------------------
    lines = []
    for emp in selected:
        mapping = {
            'name': getattr(emp, 'name', None),
            'position': getattr(emp, 'position', None),
            'department': getattr(emp, 'department', None)
        }
        # Ensure no missing attributes
        if None in mapping.values():
            raise ValueError(f"Employee '{emp}' is missing required attributes.")
        # Format the template safely
        line = _safe_format(dir_template, mapping)
        lines.append(line)

    # ------------------------------------------------------------------
    # 4. Return the final directory string
    # ------------------------------------------------------------------
    return '\n'.join(lines)

# ----------------------------------------------------------------------
# Example usage (uncomment to test):
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     EMPLOYEES.extend([
#         Employee("Alice Smith", "Engineer", "R&D", 90000, "alice@example.com"),
#         Employee("Bob Jones", "Manager", "R&D", 110000, "bob@example.com"),
#         Employee("Carol White", "Analyst", "Finance", 70000, "carol@example.com")
#     ])
#
#     template = "Employee: {name}, Position: {position}"
#     print(generate_department_directory("R&D", template))