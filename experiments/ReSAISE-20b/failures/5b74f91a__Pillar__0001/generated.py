#!/usr/bin/env python3
"""
Employee directory generator.
"""

from dataclasses import dataclass
import re
from typing import List

# --------------------------------------------------------------------------- #
# 1. Employee data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """
    Immutable representation of an employee.
    Sensitive attributes (`salary`, `personal_email`) are intentionally
    excluded from public formatting to avoid accidental leakage.
    """
    name: str
    position: str
    department: str
    # Sensitive fields are deliberately not part of the public API
    _salary: float = None          # internal use only
    _personal_email: str = None   # internal use only


# --------------------------------------------------------------------------- #
# 2. Sample data store (replace with real persistence in production)
# --------------------------------------------------------------------------- #

EMPLOYEES: List[Employee] = [
    Employee(name="Alice Smith", position="Senior Engineer",
             department="Engineering", _salary=120000.0, _personal_email="alice.smith@company.com"),
    Employee(name="Bob Johnson", position="Junior Engineer",
             department="Engineering", _salary=75000.0, _personal_email="bob.johnson@company.com"),
    Employee(name="Carol White", position="HR Manager",
             department="Human Resources", _salary=90000.0, _personal_email="carol.white@company.com"),
    # Add more employees as needed
]


# --------------------------------------------------------------------------- #
# 3. Directory building logic
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"\{employee\.([a-zA-Z_]+)\}")

# Allowed placeholders (non‑sensitive)
ALLOWED_FIELDS = {
    "name": lambda e: e.name,
    "position": lambda e: e.position,
    "department": lambda e: e.department,
}

# Forbidden placeholders
FORBIDDEN_FIELDS = {"salary", "personal_email"}


def build_team_directory(dept_name: str, format_template: str) -> str:
    """
    Build a formatted directory for all employees in the given department.

    Parameters
    ----------
    dept_name : str
        Target department name.
    format_template : str
        Template string containing placeholders like `{employee.name}`.

    Returns
    -------
    str
        A newline‑separated string of formatted employee entries.

    Raises
    ------
    ValueError
        If the template contains forbidden placeholders or if any error occurs.
    """
    # 1. Validate template for forbidden fields
    placeholders = PLACEHOLDER_PATTERN.findall(format_template)
    if any(field in FORBIDDEN_FIELDS for field in placeholders):
        raise ValueError("Template contains forbidden sensitive fields")

    # 2. Filter employees by department
    dept_employees = [e for e in EMPLOYEES if e.department.lower() == dept_name.lower()]
    if not dept_employees:
        raise ValueError(f"No employees found in department '{dept_name}'")

    # 3. Build the directory
    lines = []
    for emp in dept_employees:
        # For each placeholder, replace with the corresponding value
        def repl(match):
            field = match.group(1)
            if field not in ALLOWED_FIELDS:
                raise ValueError(f"Unknown placeholder: {{employee.{field}}}")
            return str(ALLOWED_FIELDS[field](emp))

        try:
            line = PLACEHOLDER_PATTERN.sub(repl, format_template)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to format employee data: {exc}") from exc

        lines.append(line)

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 4. Example usage (commented out; remove if using as a module)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    template = "{employee.name} - {employee.position}"
    try:
        print(build_team_directory("Engineering", template))
    except ValueError as err:
        print(f"Error: {err}")