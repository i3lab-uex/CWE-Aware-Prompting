import re
from typing import List

# ------------------------------------------------------------
# Mockup data structures (replace with actual implementations)
# ------------------------------------------------------------

class Employee:
    """Simple employee representation."""
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str):
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary          # Sensitive
        self.personal_email = personal_email  # Sensitive

# Example employee list (in real usage this would come from a DB or other source)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "R&D", 90000, "alice.smith@example.com"),
    Employee("Bob Jones", "Manager", "R&D", 120000, "bob.jones@example.com"),
    Employee("Carol White", "Analyst", "Finance", 75000, "carol.white@example.com"),
]

# ------------------------------------------------------------
# Core function
# ------------------------------------------------------------

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted directory listing for employees in the specified department.

    Parameters
    ----------
    dep : str
        Department name to filter employees.
    format_template : str
        Template string containing placeholders such as `{employee.name}`.

    Returns
    -------
    str
        Multi-line string with each employee formatted according to the template.

    Raises
    ------
    ValueError
        If the template attempts to access sensitive data (`salary` or `personal_email`)
        or if any placeholder cannot be resolved.
    """
    # ------------------------------------------------------------------
    # 1. Detect and forbid access to sensitive attributes
    # ------------------------------------------------------------------
    forbidden_attrs = {"salary", "personal_email"}
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(format_template)

    for ph in placeholders:
        # Normalize the placeholder (e.g., "employee.name" -> "name")
        parts = ph.split(".")
        if len(parts) != 2 or parts[0] != "employee":
            raise ValueError(f"Invalid placeholder format: '{{{ph}}}'")
        attr = parts[1]
        if attr in forbidden_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is prohibited")

    # ------------------------------------------------------------------
    # 2. Filter employees by department
    # ------------------------------------------------------------------
    dept_employees = [e for e in EMPLOYEES if e.department == dep]
    if not dept_employees:
        return f"No employees found in department '{dep}'."

    # ------------------------------------------------------------------
    # 3. Format each employee
    # ------------------------------------------------------------------
    lines = []
    for emp in dept_employees:
        try:
            formatted_line = format_template.format(
                employee={
                    "name": emp.name,
                    "position": emp.position,
                    # Only non-sensitive attributes are exposed
                }
            )
        except KeyError as exc:
            raise ValueError(f"Missing attribute for placeholder: {exc}") from None
        except Exception as exc:
            # Catch any other formatting errors
            raise ValueError(f"Formatting error: {exc}") from None

        lines.append(formatted_line)

    return "\n".join(lines)


# ------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------

# if __name__ == "__main__":
#     tmpl = "Name: {employee.name}, Position: {employee.position}"
#     print(generate_staff_listing("R&D", tmpl))