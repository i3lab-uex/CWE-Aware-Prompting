import re
from typing import List

# ------------------------------------------------------------------
# Sample Employee model used by the directory system.
# In a real application this would be replaced by an ORM or
# database model.  Only the attributes listed below are considered
# safe for directory output.
# ------------------------------------------------------------------
class Employee:
    def __init__(self, name: str, position: str, department: str,
                 salary: float = None, personal_email: str | None = None):
        self.name = name
        self.position = position
        self.department = department
        # Sensitive attributes (should never be exposed via the directory)
        self.salary = salary
        self.personal_email = personal_email

# ------------------------------------------------------------------
# Global list of employees.  In production this would come from a
# database or other secure store.
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = []

# ------------------------------------------------------------------
# Allowed placeholders that can appear in the directory template.
# Any other placeholder will cause a ValueError to avoid leaking
# sensitive data (CWE‑200).
# ------------------------------------------------------------------
ALLOWED_FIELDS = {"employee.name", "employee.position", "employee.department"}

PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def create_employee_directory(department: str, template: str) -> str:
    """
    Generate a directory string for all employees in the given department.

    Parameters
    ----------
    department : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders such as `{employee.name}` or
        `{employee.position}`.  The placeholders are replaced with the
        corresponding employee attribute values.

    Returns
    -------
    str
        The directory string, one entry per line.

    Raises
    ------
    ValueError
        If the template contains a placeholder that is not in
        ALLOWED_FIELDS or if any other error occurs.
    """
    try:
        # Find all placeholders in the template
        placeholders = set(PLACEHOLDER_RE.findall(template))

        # Validate that every placeholder is allowed
        for ph in placeholders:
            if f"employee.{ph}" not in ALLOWED_FIELDS:
                raise ValueError(f"Unauthorized placeholder '{ph}' detected")

        # Filter employees by department (case‑insensitive match)
        dept_employees = [
            e for e in EMPLOYEES if e.department.lower() == department.lower()
        ]

        # Build the directory output
        lines = []
        for emp in dept_employees:
            entry = template
            # Replace each placeholder with the actual value
            for ph in placeholders:
                attr = getattr(emp, ph)
                entry = entry.replace(f"{{employee.{ph}}}", str(attr))
            lines.append(entry)

        return "\n".join(lines)

    except Exception as exc:
        # Any exception is treated as a potential security issue
        raise ValueError(f"Failed to create employee directory: {exc}") from exc

# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the global list with sample data
    EMPLOYEES.extend([
        Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@example.com"),
        Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@example.com"),
        Employee("Carol Lee", "Engineer", "Design", 88000, "carol@example.com"),
    ])

    tmpl = "{employee.name} - {employee.position}"
    print(create_employee_directory("Engineering", tmpl))