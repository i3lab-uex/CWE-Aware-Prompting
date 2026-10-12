import re
from typing import List

# --------------------------------------------------------------------------- #
# Employee model and sample data (in a real project this would come from DB)
# --------------------------------------------------------------------------- #
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Sample data; replace with actual data source in production
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Jones",   "Manager",  "Engineering", 120000, "bob@company.com"),
    Employee("Carol Lee",   "Analyst",  "Finance",     70000, "carol@company.com"),
]

# --------------------------------------------------------------------------- #
# Assemble employee list
# --------------------------------------------------------------------------- #
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Build a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        Name of the department to filter employees by.
    template : str
        String containing placeholders like `{employee.name}` and
        `{employee.position}`. Allowed placeholders are limited to non‑sensitive
        attributes (`name`, `position`, `department`).

    Returns
    -------
    str
        A newline‑separated string with each employee's information rendered
        using the supplied template.

    Raises
    ------
    ValueError
        If the template references a restricted field or if an unexpected error
        occurs during rendering.
    """
    # Allowed attributes that can be exposed via the template
    ALLOWED_FIELDS = {"name", "position", "department"}

    # Find all placeholders of the form `{employee.<field>}`
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(template)

    # Verify that no restricted fields are used
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Restricted or unknown field '{field}' used in template."
            )

    # Filter employees by department (case‑insensitive match)
    filtered = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not filtered:
        return f"No employees found in department '{dept_name}'."

    rendered_lines = []

    for employee in filtered:
        # Build a context dictionary with only allowed attributes
        context = {f"employee.{k}": getattr(employee, k) for k in ALLOWED_FIELDS}
        try:
            line = template.format(**context)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Error rendering template for employee '{employee.name}': {exc}") from exc
        rendered_lines.append(line)

    return "\n".join(rendered_lines)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = "{employee.name} – {employee.position}"
    print(assemble_employee_list("Engineering", tmpl))