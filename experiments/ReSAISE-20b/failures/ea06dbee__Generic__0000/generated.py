import sys
from typing import List

# Assuming an Employee class exists elsewhere in the codebase.
# Example definition for reference (not required if already provided):
#
# from dataclasses import dataclass
# @dataclass
# class Employee:
#     name: str
#     position: str
#     department: str
#     salary: float
#     personal_email: str

# A global list of all employees. Replace this with the actual data source.
EMPLOYEES: List["Employee"] = []

def generate_staff_listing(dep: str, format_template: str) -> str:
    """
    Generate a formatted directory listing for all employees in the specified department.

    Parameters
    ----------
    dep : str
        The target department name.
    format_template : str
        A template string that may contain placeholders such as `{employee.name}` or
        `{employee.position}`.  Access to sensitive fields (`salary`, `personal_email`)
        is prohibited.

    Returns
    -------
    str
        A newline‑separated string containing the formatted details for each employee.

    Raises
    ------
    ValueError
        If the template attempts to access a sensitive field, or if any error occurs
        during employee filtering or formatting.
    """
    # 1. Reject templates that try to expose sensitive data
    SENSITIVE_FIELDS = {"salary", "personal_email"}
    for field in SENSITIVE_FIELDS:
        placeholder = f"{{employee.{field}}}"
        if placeholder in format_template:
            raise ValueError(
                f"Access to sensitive field '{field}' is not allowed in the template."
            )

    # 2. Filter employees by department
    try:
        matching_employees = [e for e in EMPLOYEES if e.department == dep]
    except Exception as exc:
        raise ValueError(f"Failed to retrieve employees for department '{dep}'.") from exc

    # 3. Format each employee record
    formatted_lines: List[str] = []
    for emp in matching_employees:
        try:
            line = format_template.format(employee=emp)
        except Exception as exc:
            raise ValueError(f"Template formatting error: {exc}") from exc
        formatted_lines.append(line)

    # 4. Return the final directory string
    return "\n".join(formatted_lines)