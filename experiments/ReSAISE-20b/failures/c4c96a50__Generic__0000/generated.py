import re
from dataclasses import dataclass, fields
from typing import List

# ----------------------------------------------------------------------
# Basic Employee model (for demonstration purposes)
# ----------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    position: str
    department: str
    salary: float          # Restricted field
    personal_email: str    # Restricted field

# Example data store – in a real application this would come from a DB
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 75000, "carol@company.com"),
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "position", "department"}
_FORBIDDEN_PLACEHOLDERS = {"salary", "personal_email"}

_placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> List[str]:
    """Return a list of field names used in the template."""
    return _placeholder_pattern.findall(template)

def _replace_placeholders(template: str, employee: Employee) -> str:
    """Replace placeholders in the template with actual employee data."""
    def repl(match: re.Match) -> str:
        field = match.group(1)
        if field in _FORBIDDEN_PLACEHOLDERS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")
        if field not in _ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder '{{employee.{field}}}' in template.")
        return str(getattr(employee, field))
    return _placeholder_pattern.sub(repl, template)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The name of the department to filter employees by.
    template : str
        A string containing placeholders like `{employee.name}` or
        `{employee.position}`.

    Returns
    -------
    str
        The concatenated string of formatted employee entries.

    Raises
    ------
    ValueError
        If the template contains a restricted field (salary or personal_email),
        an unknown placeholder, or if any unexpected error occurs during
        processing.
    """
    try:
        # Validate placeholders before processing employees
        for field in _extract_placeholders(template):
            if field in _FORBIDDEN_PLACEHOLDERS:
                raise ValueError(f"Template contains restricted placeholder '{{employee.{field}}}'.")
            if field not in _ALLOWED_FIELDS:
                raise ValueError(f"Unknown placeholder '{{employee.{field}}}' in template.")

        # Filter employees by department
        relevant_employees = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
        if not relevant_employees:
            return f"No employees found in department '{dept_name}'."

        # Build the output
        lines = [_replace_placeholders(template, emp) for emp in relevant_employees]
        return "\n".join(lines)

    except ValueError as ve:
        # Re‑raise known validation errors
        raise ve
    except Exception as exc:
        # Catch all other unexpected errors and wrap them in ValueError
        raise ValueError(f"An error occurred while assembling the employee list: {exc}") from exc