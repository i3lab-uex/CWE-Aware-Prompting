import re
from dataclasses import dataclass, fields
from typing import List

# ----------------------------------------------------------------------
# Example Employee class (replace with the actual implementation in your codebase)
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float  # restricted
    personal_email: str  # restricted

# ----------------------------------------------------------------------
# Sample data store (replace with your actual data source)
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Senior Engineer", "Engineering", 120000, "bob.johnson@example.com"),
    Employee("Carol White", "HR Manager", "Human Resources", 85000, "carol.white@example.com"),
]

# ----------------------------------------------------------------------
_RESTRICTED_FIELDS = {"salary", "personal_email"}

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference restricted fields.
    Raises ValueError if a restricted field is found or an invalid placeholder occurs.
    """
    # Find all placeholders of the form {employee.<field>}
    pattern = r"{\s*employee\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    for match in re.finditer(pattern, template):
        field_name = match.group(1)
        if field_name in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed.")
        # Ensure the field exists on Employee
        if field_name not in {f.name for f in fields(Employee)}:
            raise ValueError(f"Unknown field '{field_name}' in template.")

def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted employee directory, one entry per line.

    Raises
    ------
    ValueError
        If restricted fields are accessed, unknown placeholders are used,
        or an unexpected error occurs during formatting.
    """
    try:
        # Validate the template first
        _validate_template(template)

        # Filter employees by department (case‑insensitive)
        filtered = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]

        # Prepare the formatted lines
        lines = []
        for emp in filtered:
            # Create a simple namespace dict for formatting
            ns = {"employee": emp}
            try:
                line = template.format(**ns)
            except KeyError as exc:
                raise ValueError(f"Missing placeholder data: {exc}") from exc
            lines.append(line)

        return "\n".join(lines)
    except ValueError:
        # Re‑raise any ValueErrors we intentionally raised
        raise
    except Exception as exc:
        # Wrap unexpected errors in ValueError for consistency
        raise ValueError(f"An error occurred while assembling the employee list: {exc}") from exc