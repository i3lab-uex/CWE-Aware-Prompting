import re
from typing import List

# ------------------------------------------------------------------
# Dummy Employee model – in a real project this would come from your
# ORM or domain layer.  Only the fields that are allowed to be exposed
# are listed in the `__exposed_fields` attribute.
# ------------------------------------------------------------------
class Employee:
    __exposed_fields = {"name", "position", "department"}

    def __init__(self, name: str, position: str,
                 department: str, salary: float,
                 personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary                # restricted
        self.personal_email = personal_email  # restricted

    def to_dict(self) -> dict:
        """Return a dictionary containing only the exposed fields."""
        return {k: getattr(self, k) for k in self.__exposed_fields}


# ------------------------------------------------------------------
# Sample data – replace with your actual data source.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Lee", "Analyst", "Finance", 70000, "carol@company.com"),
    # ... more employees
]


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _check_restricted_placeholders(template: str) -> None:
    """
    Raise ValueError if the template references any restricted fields.
    Restricted fields are defined in Employee.__exposed_fields
    """
    restricted = {"salary", "personal_email"}
    for match in PLACEHOLDER_RE.finditer(template):
        field_path = match.group(1).strip()
        # Only the first segment before a dot is considered (e.g., employee.name)
        root, _, sub = field_path.partition(".")
        if root != "employee":
            raise ValueError(f"Unsupported placeholder: {field_path}")
        if sub in restricted:
            raise ValueError(f"Access to restricted field '{sub}' is not allowed.")


def _render_template(template: str, context: dict) -> str:
    """
    Safely render a template using the provided context dictionary.
    Any KeyError or formatting error results in ValueError.
    """
    try:
        return template.format(**context)
    except KeyError as e:
        raise ValueError(f"Missing field in context: {e}") from None
    except Exception as e:
        raise ValueError(f"Template rendering failed: {e}") from None


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        The department to filter employees by.
    template : str
        A format string containing placeholders such as
        '{employee.name}' and '{employee.position}'.  The template
        must not reference restricted fields like 'salary' or
        'personal_email'.

    Returns
    -------
    str
        A string containing the rendered entries for each employee in
        the department, separated by newlines.

    Raises
    ------
    ValueError
        If a restricted field is referenced in the template,
        or if an unexpected error occurs during rendering.
    """
    # Validate that no restricted fields are used
    _check_restricted_placeholders(template)

    # Filter employees by department (case‑insensitive match)
    dept_employees = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    # Build the output
    rendered_lines = []
    for emp in dept_employees:
        context = {"employee": emp.to_dict()}
        rendered_lines.append(_render_template(template, context))

    return "\n".join(rendered_lines)


# ------------------------------------------------------------------
# Example usage (commented out – remove to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    print(assemble_employee_list("Engineering", tmpl))