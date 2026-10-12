#!/usr/bin/env python3
"""
Employee directory generator.

The module assumes a global iterable ``EMPLOYEES`` that contains instances
of :class:`Employee`.  Only the attributes ``name``, ``position`` and
``department`` are allowed to be interpolated into the roster template.
Accessing restricted fields such as ``salary`` or ``personal_email`` will
raise a :class:`ValueError`.

The function is intentionally written to avoid leaking resources and
to be resistant against accidental template injection.
"""

from __future__ import annotations

import re
from typing import Iterable, List


# --------------------------------------------------------------------------- #
#  Employee model (minimal implementation for illustration)
# --------------------------------------------------------------------------- #

class Employee:
    """
    A simple employee data holder.
    """

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

    def __repr__(self) -> str:
        return (
            f"Employee(name={self.name!r}, position={self.position!r}, "
            f"department={self.department!r})"
        )


# --------------------------------------------------------------------------- #
#  Global employee collection
# --------------------------------------------------------------------------- #

# In a real application this would be populated from a database or file.
EMPLOYEES: List[Employee] = [
    Employee("Alice Smith", "Engineer", "Engineering", 95000, "alice.smith@company.com"),
    Employee("Bob Johnson", "Manager", "Engineering", 120000, "bob.johnson@company.com"),
    Employee("Carol Williams", "Analyst", "Finance", 70000, "carol.williams@company.com"),
    # ... more employees ...
]


# --------------------------------------------------------------------------- #
#  Roster generation
# --------------------------------------------------------------------------- #

_REPLACE_PATTERN = re.compile(r"\{employee\.([^\}]+)\}")
_RESTRICTED_FIELDS = {"salary", "personal_email"}


def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any restricted fields.
    Raises ValueError if a forbidden field is detected.
    """
    for match in _REPLACE_PATTERN.finditer(template):
        attr = match.group(1)
        if attr in _RESTRICTED_FIELDS:
            raise ValueError(
                f"Access to restricted field '{attr}' is not allowed in the template."
            )


def _render_employee(template: str, employee: Employee) -> str:
    """
    Render the template for a single employee.
    Unsafe attributes are already checked by `_validate_template`.
    """
    result = template
    for match in _REPLACE_PATTERN.finditer(template):
        attr = match.group(1)
        # Safely fetch attribute; default to empty string if missing
        value = getattr(employee, attr, "")
        # Convert non-string values to str for interpolation
        result = result.replace(match.group(0), str(value))
    return result


def generate_team_roster(
    division_name: str,
    roster_template: str,
) -> str:
    """
    Generate a formatted employee directory for the specified department.

    Parameters
    ----------
    division_name : str
        The name of the department to filter employees by.
    roster_template : str
        A string template containing placeholders such as `{employee.name}`
        and `{employee.position}`.

    Returns
    -------
    str
        A newline‑separated string containing the rendered roster for each
        employee in the specified department.

    Raises
    ------
    ValueError
        If the template attempts to access restricted fields or if an
        unexpected error occurs during rendering.
    """
    try:
        # 1. Validate template against restricted fields
        _validate_template(roster_template)

        # 2. Filter employees by department (case‑insensitive match)
        filtered: Iterable[Employee] = (
            emp for emp in EMPLOYEES if emp.department.lower() == division_name.lower()
        )

        # 3. Render each employee entry
        rendered_entries: List[str] = [
            _render_employee(roster_template, emp) for emp in filtered
        ]

        # 4. Join with newline separators; empty string if no matches
        return "\n".join(rendered_entries)

    except Exception as exc:
        # Convert any unexpected exception into a ValueError with context
        raise ValueError(f"Failed to generate roster: {exc}") from exc


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Name: {employee.name}, Position: {employee.position}"
    print(generate_team_roster("Engineering", template))