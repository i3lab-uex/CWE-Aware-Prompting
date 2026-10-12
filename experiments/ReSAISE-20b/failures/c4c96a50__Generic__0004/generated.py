import re
from typing import List

# Assume an Employee class exists with the following attributes:
# name, position, department, salary, personal_email
# For demonstration purposes we define a minimal stub.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# Global list of all employees (would normally come from a database or similar)
ALL_EMPLOYEES: List[Employee] = []


def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders in the form `{employee.<field>}`.

    Returns
    -------
    str
        The concatenated formatted strings for each employee in the department.

    Raises
    ------
    ValueError
        If the template references a restricted field (`salary` or `personal_email`)
        or if any other error occurs during formatting.
    """
    # Pre-compile the regex to find placeholders
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Find all unique fields used in the template
    fields = set(match.group(1) for match in placeholder_pattern.finditer(template))

    # Restrict access to sensitive fields
    restricted = {"salary", "personal_email"}
    if any(field in restricted for field in fields):
        raise ValueError(f"Template references restricted field(s): "
                         f"{', '.join(restricted & fields)}")

    # Build a list of formatted lines
    formatted_lines = []

    for emp in ALL_EMPLOYEES:
        if emp.department != dept_name:
            continue

        # Prepare a mapping for allowed fields
        context = {}
        for field in fields:
            try:
                value = getattr(emp, field)
            except AttributeError as exc:
                raise ValueError(f"Employee has no attribute '{field}'.") from exc
            context[field] = value

        try:
            formatted_line = template.format(**context)
        except Exception as exc:  # Catch any formatting errors
            raise ValueError(f"Error formatting template for employee {emp.name}: "
                             f"{exc}") from exc

        formatted_lines.append(formatted_line)

    return "\n".join(formatted_lines)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     ALL_EMPLOYEES.extend([
#         Employee("Alice", "Engineer", "Engineering", 95000, "alice@example.com"),
#         Employee("Bob", "Manager", "Engineering", 120000, "bob@example.com"),
#         Employee("Carol", "Analyst", "Finance", 70000, "carol@example.com"),
#     ])
#
#     tmpl = "{employee.name} - {employee.position}"
#     print(assemble_employee_list("Engineering", tmpl))