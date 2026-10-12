import re
from typing import List

# ------------------------------------------------------------------
# Employee model (minimal implementation for the example)
# ------------------------------------------------------------------
class Employee:
    """
    Simple employee data container.

    Attributes
    ----------
    name : str
        Full name of the employee.
    position : str
        Job title.
    department : str
        Department name.
    salary : float
        Annual salary (restricted).
    personal_email : str
        Personal e‑mail address (restricted).
    """
    def __init__(self, name: str, position: str, department: str,
                 salary: float, personal_email: str) -> None:
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email


# ------------------------------------------------------------------
# Global employee list (in a real system this would come from a DB)
# ------------------------------------------------------------------
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 115000, "bob@example.com"),
    Employee("Carol White", "Analyst", "Finance", 70000, "carol@example.com"),
    # ... more employees
]


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Compile a directory of employees for a given department using the supplied
    template. Restricted fields (salary and personal_email) are disallowed.

    Parameters
    ----------
    dept_name : str
        Department name to filter employees.
    template : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        Formatted directory string. Each employee occupies a line.

    Raises
    ------
    ValueError
        If the template attempts to use restricted fields or an unexpected error occurs.
    """
    # --------------------------------------------------------------
    # Validate template for restricted placeholders
    # --------------------------------------------------------------
    # Find all placeholders in the form {employee.<field>}
    placeholder_pattern = re.compile(r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(template)

    # Restricted fields
    restricted_fields = {"salary", "personal_email"}

    for field in placeholders:
        if field in restricted_fields:
            raise ValueError(
                f"Template contains disallowed placeholder '{{employee.{field}}}'. "
                "Access to restricted fields is prohibited."
            )

    # --------------------------------------------------------------
    # Filter employees by department
    # --------------------------------------------------------------
    filtered_emps = [
        emp for emp in EMPLOYEES if emp.department.lower() == dept_name.lower()
    ]

    # --------------------------------------------------------------
    # Build output
    # --------------------------------------------------------------
    lines = []
    try:
        for emp in filtered_emps:
            # Prepare a namespace for formatting
            context = {"employee": emp}
            line = template.format(**context)
            lines.append(line)
    except Exception as exc:
        # Any formatting error is treated as a security violation
        raise ValueError(f"Failed to format employee data: {exc}") from exc

    return "\n".join(lines)