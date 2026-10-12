#!/usr/bin/env python3
"""
Utility to assemble an employee directory from a template.

The module assumes the existence of an ``Employee`` class with the
attributes:
    - name (str)
    - position (str)
    - department (str)
    - salary (float)
    - personal_email (str)

The function ``assemble_employee_list`` filters employees by
department and substitutes placeholders in the form ``{employee.<field>}``
with the corresponding attribute values.  Access to restricted
attributes (``salary`` and ``personal_email``) is prohibited.

Any attempt to reference a restricted field or any unexpected error
results in a ``ValueError`` being raised.
"""

from __future__ import annotations

import re
from typing import Iterable, List

# --------------------------------------------------------------------------- #
# Mock / placeholder Employee class and data source
# In real usage replace this with the actual implementation.
# --------------------------------------------------------------------------- #
class Employee:
    """Simple employee data holder."""
    def __init__(self, name: str, position: str,
                 department: str, salary: float,
                 personal_email: str) -> None:
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.personal_email = personal_email

# Example data source; in real code this would be replaced by a DB query or similar.
_EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@example.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob.johnson@example.com"),
    Employee("Carol Lee", "Analyst", "Finance", 75000, "carol.lee@example.com"),
]

def get_all_employees() -> Iterable[Employee]:
    """Return an iterable of all employees."""
    return _EMPLOYEES


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the given department.

    Parameters
    ----------
    dept_name : str
        Department name to filter employees.
    template : str
        Template string containing placeholders of the form
        ``{employee.<field>}``. Allowed fields are:
            * name
            * position
            * department

    Returns
    -------
    str
        The assembled directory, each employee on its own line.

    Raises
    ------
    ValueError
        If a restricted field is referenced or any unexpected error occurs.
    """
    # Allowed fields that can be substituted
    allowed_fields = {"name", "position", "department"}

    # Regex to find placeholders like {employee.name}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    lines: List[str] = []

    try:
        for emp in get_all_employees():
            if emp.department.lower() != dept_name.lower():
                continue

            # Validate placeholders
            def replace_match(match: re.Match[str]) -> str:
                field = match.group(1)
                if field not in allowed_fields:
                    raise ValueError(
                        f"Restricted or unknown employee field '{field}' "
                        "access attempted in template."
                    )
                return str(getattr(emp, field))

            try:
                line = placeholder_pattern.sub(replace_match, template)
            except ValueError as ve:
                # Re-raise to propagate restricted field error
                raise ve
            except Exception as exc:
                # Any other formatting error is considered unexpected
                raise ValueError(
                    f"Unexpected error while processing template: {exc}"
                ) from exc

            lines.append(line)

        return "\n".join(lines)
    except ValueError:
        # Propagate known errors
        raise
    except Exception as exc:
        # Unexpected runtime errors
        raise ValueError(f"Unexpected error in assemble_employee_list: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        output = assemble_employee_list("Engineering", tmpl)
        print(output)
    except ValueError as e:
        print(f"Error: {e}")