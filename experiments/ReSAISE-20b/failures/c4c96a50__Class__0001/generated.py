#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility to assemble an employee directory for a specific department.
"""

import re
from typing import List

# ----------------------------------------------------------------------
# The Employee model is expected to be defined elsewhere in the project.
# For the purpose of this module we only need a minimal protocol that
# provides the attributes used in the template.
# ----------------------------------------------------------------------
class Employee:
    """
    Minimal protocol for an employee object.

    Attributes
    ----------
    name : str
        Full name of the employee.
    position : str
        Job title or role within the company.
    department : str
        Department name where the employee works.
    salary : float
        Annual salary (sensitive, must not be exposed).
    personal_email : str
        Personal email address (sensitive, must not be exposed).
    """
    name: str
    position: str
    department: str
    salary: float  # Sensitive
    personal_email: str  # Sensitive


# ----------------------------------------------------------------------
# In a real application this function would query a database or other
# data store. Here we provide a simple placeholder that can be replaced.
# ----------------------------------------------------------------------
def get_all_employees() -> List[Employee]:
    """
    Return a list of all Employee objects.

    This is a stub. Replace with real data retrieval logic.
    """
    # Example placeholder data
    return [
        Employee.__new__(Employee, name="Alice Smith", position="Engineer",
                         department="Engineering", salary=95000.0,
                         personal_email="alice.smith@example.com"),
        Employee.__new__(Employee, name="Bob Jones", position="Manager",
                         department="Engineering", salary=120000.0,
                         personal_email="bob.jones@example.com"),
        Employee.__new__(Employee, name="Carol White", position="Analyst",
                         department="Finance", salary=85000.0,
                         personal_email="carol.white@example.com"),
    ]


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def assemble_employee_list(dept_name: str, template: str) -> str:
    """
    Assemble a formatted employee directory for the specified department.

    Parameters
    ----------
    dept_name : str
        The department name to filter employees by.
    template : str
        A string containing placeholders in the form '{employee.<field>}'.

    Returns
    -------
    str
        The formatted directory string, with one line per employee.

    Raises
    ------
    ValueError
        If the template attempts to access restricted fields (salary or personal_email)
        or if an unexpected error occurs during processing.
    """
    # Regular expression to find placeholders of the form {employee.field}
    placeholder_pattern = re.compile(r"\{employee\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    # Identify all placeholders used in the template
    try:
        fields_in_template = set(placeholder_pattern.findall(template))
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to parse template placeholders: {exc}") from exc

    # Restrict access to sensitive fields
    restricted = {"salary", "personal_email"}
    if restricted & fields_in_template:
        raise ValueError(
            f"Template contains disallowed fields: {restricted & fields_in_template}"
        )

    # Retrieve employees and filter by department
    all_emps = get_all_employees()
    dept_emps = [e for e in all_emps if e.department == dept_name]

    # If no employees found, return an empty string
    if not dept_emps:
        return ""

    # Prepare a function that substitutes placeholders for a single employee
    def substitute_for_employee(emp: Employee) -> str:
        try:
            result = template
            for field in fields_in_template:
                # Use getattr safely; if attribute missing, raise ValueError
                try:
                    value = getattr(emp, field)
                except AttributeError as exc:  # pragma: no cover
                    raise ValueError(
                        f"Employee object missing required attribute '{field}'"
                    ) from exc
                # Convert value to string (handles numbers, etc.)
                result = result.replace(f"{{employee.{field}}}", str(value))
            return result
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to substitute placeholders: {exc}") from exc

    # Build the final directory string
    try:
        lines = [substitute_for_employee(emp) for emp in dept_emps]
        return "\n".join(lines)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Unexpected error while assembling directory: {exc}") from exc


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Name: {employee.name}, Position: {employee.position}"
    try:
        output = assemble_employee_list("Engineering", tmpl)
        print(output)
    except ValueError as e:
        print(f"Error: {e}")