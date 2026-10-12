#!/usr/bin/env python3
"""
Utility to assemble an employee directory based on a template.
"""

from dataclasses import dataclass
import string
from typing import List

# --------------------------------------------------------------------------- #
# Employee model (minimal for this example)
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Restricted field
    personal_email: str    # Restricted field

# --------------------------------------------------------------------------- #
# Sample data – in a real system this would come from a database or API
# --------------------------------------------------------------------------- #
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Software Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Product Manager", "Engineering", 105000, "bob.johnson@example.com"),
    Employee("Carol Lee", "HR Specialist", "Human Resources", 70000, "carol.lee@example.com"),
]

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The department name to filter employees by.
    template : str
        A string containing placeholders of the form `{employee.<field>}`.

    Returns
    -------
    str
        The formatted employee directory, with one line per employee.

    Raises
    ------
    ValueError
        If the template references restricted fields (`salary`, `personal_email`)
        or if an unexpected error occurs.
    """
    # Allowed fields that can be referenced in the template
    ALLOWED_FIELDS = {"name", "position", "department"}

    # Identify placeholders in the template
    formatter = string.Formatter()
    try:
        fields_in_template = set()
        for literal_text, field_name, format_spec, conversion in formatter.parse(template):
            if field_name is None:
                continue
            # Expect format like 'employee.name'
            parts = field_name.split(".")
            if len(parts) != 2 or parts[0] != "employee":
                raise ValueError(f"Unsupported placeholder: '{{{field_name}}}'")
            field = parts[1]
            if field not in ALLOWED_FIELDS:
                raise ValueError(f"Access to restricted field '{field}' is prohibited.")
            fields_in_template.add(field)
    except Exception as exc:
        raise ValueError(f"Error parsing template: {exc}") from exc

    # Filter employees by department
    filtered = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not filtered:
        return f"No employees found in department '{dept_name}'."

    # Build formatted lines
    lines = []
    for emp in filtered:
        try:
            # Construct a mapping for the template
            context = {"employee": emp}
            line = template.format(**context)
            lines.append(line)
        except Exception as exc:
            raise ValueError(f"Failed to format employee '{emp.name}': {exc}") from exc

    return "\n".join(lines)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    print(assemble_employee_list("Engineering", tmpl))