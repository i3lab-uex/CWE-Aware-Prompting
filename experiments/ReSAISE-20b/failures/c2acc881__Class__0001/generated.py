import re
from typing import List

# Assume an Employee class is defined elsewhere in the project with at least these attributes.
# from employee_module import Employee

# For demonstration purposes we define a minimal Employee dataclass here.
# Remove or replace this with the real import in your codebase.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Global list of employees (replace with your actual data source).
EMPLOYEES: List[Employee] = []


def compile_department_roster(division: str, template_str: str) -> str:
    """
    Generate a formatted employee directory for the specified division.

    Parameters
    ----------
    division : str
        The department name to filter employees.
    template_str : str
        A string containing placeholders such as '{employee.name}' or
        '{employee.position}'. Placeholders that refer to sensitive data
        (salary, personal_email) are disallowed.

    Returns
    -------
    str
        A newline‑separated string where each line is the formatted template
        for one employee in the requested division.

    Raises
    ------
    ValueError
        If any placeholder references sensitive data or if an error occurs
        during formatting.
    """
    # 1. Check for disallowed placeholders (sensitive fields).
    sensitive_fields = {"salary", "personal_email"}
    # Find all placeholders in the template. Example: {employee.name}
    placeholder_pattern = re.compile(r"{([^}]+)}")
    placeholders = set(placeholder_pattern.findall(template_str))

    # Remove the 'employee.' prefix if present
    for key in list(placeholders):
        if key.startswith("employee."):
            placeholders.remove(key)
            placeholders.add(key.split(".", 1)[1])

    # If any sensitive field is referenced, raise an error.
    if placeholders & sensitive_fields:
        bad = ", ".join(sorted(placeholders & sensitive_fields))
        raise ValueError(f"Access to sensitive fields not allowed: {bad}")

    # 2. Filter employees by division.
    filtered = [e for e in EMPLOYEES if e.department.lower() == division.lower()]
    if not filtered:
        return ""

    # 3. Prepare the formatted lines.
    formatted_lines = []
    for emp in filtered:
        # Build a mapping of allowed attributes
        attr_map = {
            "name": getattr(emp, "name", None),
            "position": getattr(emp, "position", None),
        }

        # Ensure all placeholders exist in the mapping
        missing = placeholders - attr_map.keys()
        if missing:
            raise ValueError(f"Missing attributes for placeholders: {', '.join(missing)}")

        try:
            line = template_str.format(**attr_map)
        except Exception as exc:
            raise ValueError(f"Error formatting template for employee '{emp.name}': {exc}") from exc

        formatted_lines.append(line)

    return "\n".join(formatted_lines)