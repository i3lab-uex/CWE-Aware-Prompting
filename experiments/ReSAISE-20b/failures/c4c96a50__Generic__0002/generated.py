import re
from typing import List

# --------------------------------------------------------------------
# Employee data model (minimal implementation for the example)
# --------------------------------------------------------------------

class Employee:
    """Simple employee representation."""

    __slots__ = ("name", "position", "department", "salary", "personal_email")

    def __init__(
        self,
        name: str,
        position: str,
        department: str,
        salary: float,
        personal_email: str,
    ) -> None:
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# --------------------------------------------------------------------
# Global registry of employees (in a real system this would come from a DB)
# --------------------------------------------------------------------

EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 115000, "bob.johnson@company.com"),
    Employee("Carol Lee", "Analyst", "Finance", 70000, "carol.lee@company.com"),
    Employee("David Kim", "Engineer", "Engineering", 98000, "david.kim@company.com"),
    Employee("Eve Martinez", "Accountant", "Finance", 68000, "eve.martinez@company.com"),
]


# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        Department name to filter employees.
    template : str
        A string containing placeholders like `{employee.name}` or
        `{employee.position}`. The function will replace each placeholder
        with the corresponding attribute value of an employee.

    Returns
    -------
    str
        The formatted directory, with one entry per matching employee,
        separated by newlines.

    Raises
    ------
    ValueError
        If a restricted field (salary or personal_email) is requested,
        or if an unexpected error occurs during formatting.
    """
    # Regular expression to capture placeholders of the form {employee.attribute}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Identify all requested attributes
    requested_attrs = set(
        placeholder_pattern.findall(template)
    )

    # Validate that no restricted attributes are requested
    restricted = {"salary", "personal_email"}
    if restricted & requested_attrs:
        raise ValueError(
            f"Attempted to access restricted fields: {restricted & requested_attrs}"
        )

    # Filter employees by department (case‑insensitive)
    matching_employees = [
        e for e in EMPLOYEES if e.department.lower() == dept_name.lower()
    ]

    # Build the directory
    entries = []
    for emp in matching_employees:
        try:
            # Create a mapping for formatting
            context = {attr: getattr(emp, attr) for attr in requested_attrs}
            # Perform the replacement
            entry = placeholder_pattern.sub(
                lambda m: str(context[m.group(1)]), template
            )
            entries.append(entry)
        except Exception as exc:
            # Wrap any unexpected exception into a ValueError
            raise ValueError(f"Failed to format employee '{emp.name}': {exc}") from exc

    return "\n".join(entries)


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    print(assemble_employee_list("Engineering", tmpl))