import re
from typing import List

# ------------------------------------------------------------
# Example Employee model (minimal implementation for context)
# ------------------------------------------------------------

class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------
# Sample data (would normally come from a database or API)
# ------------------------------------------------------------

EMPLOYEES: List[Employee] = [
    Employee("Alice Johnson", "Engineer", "R&D", 95000.0, "alice.j@company.com"),
    Employee("Bob Smith",     "Analyst",  "Finance", 75000.0, "bob.s@company.com"),
    Employee("Carol Lee",     "Manager",  "R&D",     105000.0, "carol.l@company.com"),
    # ... more employees ...
]

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------

def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        Department name to filter employees.
    template : str
        String containing placeholders in the form {employee.<field>}.

    Returns
    -------
    str
        Concatenated string with each employee's details substituted into the template.

    Raises
    ------
    ValueError
        If restricted fields are accessed or an unexpected error occurs.
    """
    # Define which employee attributes are not allowed to be exposed
    restricted_fields = {"salary", "personal_email"}

    # Regular expression to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Filter employees by department (case-insensitive match)
    filtered_employees = [
        emp for emp in EMPLOYEES
        if emp.department.lower() == dept_name.strip().lower()
    ]

    if not filtered_employees:
        return f"No employees found in department '{dept_name}'."

    lines = []

    for emp in filtered_employees:
        try:
            # Function to replace each placeholder with the actual value
            def replacer(match: re.Match) -> str:
                field_name = match.group(1)
                if field_name in restricted_fields:
                    raise ValueError(
                        f"Access to restricted field '{field_name}' is prohibited."
                    )
                if not hasattr(emp, field_name):
                    raise ValueError(
                        f"Employee has no attribute '{field_name}'."
                    )
                value = getattr(emp, field_name)
                return str(value)

            # Perform substitution
            line = placeholder_pattern.sub(replacer, template)
            lines.append(line)

        except Exception as exc:
            # Any exception (including ValueError) is wrapped and re-raised
            raise ValueError(
                f"Failed to assemble employee list for '{emp.name}': {exc}"
            ) from exc

    # Join all lines with newline separator
    return "\n".join(lines)

# ------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(assemble_employee_list("R&D", tmpl))