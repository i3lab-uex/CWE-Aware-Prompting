import re
from typing import List

# Minimal Employee class used for illustration. In real usage this would be imported.
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary          # Sensitive
        self.personal_email = personal_email  # Sensitive


# Example employee database (in a real application this would come from a DB or API)
EMPLOYEE_DB: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000.0, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000.0, "bob.johnson@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 80000.0, "carol.williams@company.com"),
    # ... more employees
]


def _extract_placeholders(template: str) -> List[str]:
    """
    Extracts all placeholder names of the form {employee.<field>} from the template.
    """
    pattern = r"\{employee\.([^\}]+)\}"
    return re.findall(pattern, template)


def _validate_template(placeholders: List[str]) -> None:
    """
    Ensures that no sensitive fields are requested in the template.
    Raises ValueError if a forbidden field is found.
    """
    forbidden = {"salary", "personal_email"}
    for field in placeholders:
        if field in forbidden:
            raise ValueError(f"Access to sensitive field '{field}' is prohibited.")


def _format_employee(employee: Employee, template: str) -> str:
    """
    Safely formats a single employee using the provided template.
    Only non‑sensitive fields are allowed.
    """
    # Build a mapping for format_map
    mapping = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department
    }
    try:
        return template.format_map(mapping)
    except KeyError as exc:
        raise ValueError(f"Missing field in template: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Template formatting error: {exc}") from None


def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generates a directory listing for all employees in the specified department.

    Parameters
    ----------
    dep : str
        The target department name.
    format_template : str
        A template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        A newline‑separated string of formatted employee entries.

    Raises
    ------
    ValueError
        If the template tries to access sensitive data or if formatting fails.
    """
    # Validate template once
    placeholders = _extract_placeholders(format_template)
    _validate_template(placeholders)

    # Filter employees by department (case‑insensitive match)
    matched = [e for e in EMPLOYEE_DB if e.department.lower() == dep.lower()]
    if not matched:
        return f"No employees found in department '{dep}'."

    # Build output
    lines = []
    for emp in matched:
        line = _format_employee(emp, format_template)
        lines.append(line)

    return "\n".join(lines)


# Example usage:
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_staff_listing("Engineering", template))