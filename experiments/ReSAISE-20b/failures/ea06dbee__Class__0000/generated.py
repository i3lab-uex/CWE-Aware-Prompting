import re
from typing import List

# ----------------------------------------------------------------------
# Dummy Employee class – in real usage this would be imported from your
# application's data model.  Only the public attributes are exposed.
# ----------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        # Sensitive fields are intentionally *not* attributes that can be
        # accessed via the template.
        self._salary = salary
        self._personal_email = personal_email

    # Properties for non‑sensitive data only.
    @property
    def salary(self):
        raise AttributeError("Access to salary is forbidden")

    @property
    def personal_email(self):
        raise AttributeError("Access to personal email is forbidden")


# ----------------------------------------------------------------------
# Sample data – replace with your real employee list.
# ----------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Developer", "Engineering", 90000, "alice@example.com"),
    Employee("Bob Johnson", "Designer", "Design", 80000, "bob@example.com"),
    Employee("Carol Williams", "Manager", "Engineering", 120000, "carol@example.com"),
]


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted employee directory for the given department.

    Parameters
    ----------
    dep : str
        Department name to filter employees by.
    format_template : str
        Template containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        A newline‑separated string of formatted employee entries.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive fields or if any other
        exception occurs during formatting.
    """
    # 1. Ensure the template does not reference sensitive data.
    _sensitive_fields = {"salary", "personal_email"}
    placeholder_pattern = re.compile(r"\{employee\.([^\}]+)\}")
    for match in placeholder_pattern.finditer(format_template):
        field = match.group(1).strip()
        if field in _sensitive_fields:
            raise ValueError(f"Template attempts to expose sensitive data: '{field}'")

    # 2. Filter employees by department.
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dep.lower()]
    if not dept_employees:
        return ""  # No employees found for the department.

    # 3. Format each employee.
    formatted_lines = []
    for emp in dept_employees:
        try:
            # Build a simple namespace dictionary.
            ns = {"employee": emp}
            formatted_line = format_template.format(**ns)
        except Exception as exc:
            raise ValueError(f"Error formatting employee '{emp.name}': {exc}") from exc
        formatted_lines.append(formatted_line)

    return "\n".join(formatted_lines)


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_staff_listing("Engineering", template))