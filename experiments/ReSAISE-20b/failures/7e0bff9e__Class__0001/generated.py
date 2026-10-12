# -*- coding: utf-8 -*-
"""
Utility to generate a performance report for an employee using a template string.
The function validates that only non‑sensitive fields are used in the template
and raises ValueError if a disallowed field is requested.
"""

import string
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
#  Sample data structures (in a real system these would be retrieved from DB)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    code: str          # unique employee identifier
    name: str
    position: str
    department: str

@dataclass
class Performance:
    employee_code: str  # foreign key to Employee.code
    rating: float       # numeric score, e.g. 4.5
    feedback: str       # sensitive text
    bonus: float        # monetary amount

# In-memory mock data stores
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(code="E001", name="Alice Smith", position="Senior Engineer", department="R&D"),
    "E002": Employee(code="E002", name="Bob Johnson", position="Product Manager", department="Marketing"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_code="E001", rating=4.7, feedback="Excellent teamwork.", bonus=1200.00),
    "E002": Performance(employee_code="E002", rating=4.2, feedback="Strong leadership.", bonus=950.00),
}

# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #

def _get_employee(emp_code: str) -> Employee:
    """Retrieve an Employee object, raising ValueError if not found."""
    emp = EMPLOYEES.get(emp_code)
    if not emp:
        raise ValueError(f"Employee with code '{emp_code}' not found.")
    return emp

def _get_performance(emp_code: str) -> Performance:
    """Retrieve a Performance object, raising ValueError if not found."""
    perf = PERFORMANCES.get(emp_code)
    if not perf:
        raise ValueError(f"Performance data for employee '{emp_code}' not found.")
    return perf

# --------------------------------------------------------------------------- #
#  Core function
# --------------------------------------------------------------------------- #

ALLOWED_EMP_FIELDS = {"name", "position", "department"}
ALLOWED_PERF_FIELDS = {"rating"}

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report string for the given employee.

    Parameters
    ----------
    emp_code : str
        The unique identifier of the employee.
    summary_template : str
        A format string containing placeholders such as '{employee.name}',
        '{employee.position}', and '{performance.rating}'.  Placeholders for
        sensitive fields (e.g., feedback, bonus) are not allowed.

    Returns
    -------
    str
        The formatted performance report string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, or if the template
        references disallowed fields.
    """
    # Retrieve data
    employee = _get_employee(emp_code)
    performance = _get_performance(emp_code)

    # Parse the template to identify all placeholders
    formatter = string.Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(summary_template):
        if not field_name:
            continue  # No placeholder
        # Split by dot to identify the object and attribute
        parts = field_name.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid placeholder '{field_name}'. Expected format '{{object.attribute}}'.")
        obj, attr = parts
        if obj == "employee":
            if attr not in ALLOWED_EMP_FIELDS:
                raise ValueError(f"Access to restricted employee field '{attr}' is not allowed.")
        elif obj == "performance":
            if attr not in ALLOWED_PERF_FIELDS:
                raise ValueError(f"Access to restricted performance field '{attr}' is not allowed.")
        else:
            raise ValueError(f"Unknown placeholder object '{obj}'. Only 'employee' and 'performance' are supported.")

    # Build the mapping for formatting
    context = {
        "employee": employee,
        "performance": performance
    }

    # Perform safe formatting
    try:
        result = summary_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Error formatting template: {exc}") from None

    return result


# --------------------------------------------------------------------------- #
#  Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "----------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5\n"
    )
    print(create_performance_report("E001", template))